import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from MKscrapy.items import MKSaleProductItem


class MKspider(scrapy.Spider):
    name = 'MKspider'
    color_numbers = 0

    def start_requests(self):
        urls = [
            "https://www.michaelkors.com/sale/handbags/_/N-289z",
            "https://www.michaelkors.com/women/handbags/_/N-8uqea5" # 这个可能是会经常变动的
        ]
        for url in urls:
            yield Request(url, self.parse)

    def parse(self, response):

        f = open('all_sales_html.html', 'w')  # 储存抓取到的原始html
        f.write(response.text)
        bs = BeautifulSoup(response.text, 'lxml')
        have_sale_count = int(bs.find('span', class_='product-count').contents[0])  # 实际打折包数量
        products = bs.find_all('li', class_='product-tile left small-6 medium-3')  # 每一个对应一个打折包所在的标签
        get_sale_count = len(products)  # 抓取到的打折包的数量

        if have_sale_count == get_sale_count:
            print('Have gotten every product! Have:', have_sale_count, 'Get:', get_sale_count)
        else:
            print('Missing some products! Have:', have_sale_count, 'Get:', get_sale_count)

        for product in products[10:20]:
            item = MKSaleProductItem()
            if product.find('div', class_='salePrice') is None:  # 本商品无折扣，跳过
                continue
            link_tag = product.find('li', class_="product-name-container").find('a')
            item['style_id'] = link_tag['href'].split('_')[-1]
            item['product_name'] = link_tag.get_text()
            item['details_url'] = link_tag['href']
            item['list_price'] = product.find('div', class_='listPrice').find_all('span', class_="ada-link")[
                1].get_text()
            item['sale_price'] = product.find('div', class_='salePrice').find_all('span', class_="ada-link")[
                1].get_text()
            if product.strong is None:
                item['is_limited_sale'] = False
            else:
                item['is_limited_sale'] = True
            item['show_img'] = 'https:' + product.find('div', class_='product-image-container').find('img')['data-src']

            yield Request(item['details_url'], callback=self.parse_details, meta={'item': item})

    def parse_details(self, response):
        bs_detail = BeautifulSoup(response.text, 'lxml')
        item = response.meta['item']
        if bs_detail.find('div', class_="product-not-available") is not None:
            item['is_available_now'] = False
            yield item
        else:
            item['is_available_now'] = True
            item['design_description'] = bs_detail.find('p', class_="design", itemprop="description").get_text()
            #  如果有回车格要去掉
            item['details'] = bs_detail.find('div', class_="detail").get_text().replace("\n", "").split("\u2022")[1:]
            item['materials'] = item['details'][0].strip()  # 材质, details每行以空格开始，所以用'[2:]'取出有用信息
            item['size'] = item['details'][2].strip()  # 尺寸
            review = bs_detail.find('span', itemprop="reviewCount")
            if review is None:
                item['review_count'] = 0
            else:
                item['review_count'] = int(review.get_text())
                item['rate_value'] = float(bs_detail.find('span', itemprop="ratingValue").get_text())

            sale_message = bs_detail.find('div', id="monetate_selectorHTML_ecc8de11_0")
            if sale_message is not None:
                item['sale_message'] = sale_message.get_text()
                item['sale_deadline'] = sale_message.get_text().split('.')[-2]
            color_div = bs_detail.find('div', class_="color-container")
            if color_div is not None:
                colors = []
                tags = color_div.find_all('label')
                for tag in tags:
                    color_id = tag['for'].split('-')[1]
                    color_url = tag['style'].split("\"")[-2]
                    color = {'id': color_id, 'name': tag['title'], 'url': color_url}
                    colors.append(color)
                item['available_colors'] = colors
            if item['sale_price'].__contains__('-'):
                for item_color in item['available_colors']:
                    url_with_color = item['details_url'] + "?color=" + item_color['id']
                    yield Request(url_with_color, callback=self.parse_color_price,
                                  meta={'item': item, 'id': item_color['id']})
            else:
                yield item

    def parse_color_price(self, response):
        bs_color = BeautifulSoup(response.text, 'lxml')
        item = response.meta['item']
        color_id = response.meta['id']
        count = 0
        for c in item['available_colors']:
            if c['id'] == color_id:
                c['sale_price'] = bs_color.find('div', class_='salePrice').find_all('span', class_="ada-link")[
                    1].get_text()
            if 'sale_price' in c:
                count += 1
        if count == len(item['available_colors']):
            yield item
