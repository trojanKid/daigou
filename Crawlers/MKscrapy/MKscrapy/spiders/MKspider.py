import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from MKscrapy.items import MKSaleProductItem


class MKspider(scrapy.Spider):
    name = 'MKspider'

    def start_requests(self):
        urls = [
            "https://www.michaelkors.com/sale/handbags/_/N-289z"
        ]
        for url in urls:
            yield Request(url, self.parse)

    def parse(self, response):
        item = MKSaleProductItem()
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

        detail_urls = []  # 下一步要请求的详细信息的清单

        for product in products:
            link_tag = product.find('li', class_="product-name-container").find('a')
            item['style_id'] = link_tag['href'].split('_')[-1]
            item['product_name'] = link_tag.get_text()
            item['details_url'] = link_tag['href']
            detail_urls.append(item['details_url'])
            item['list_price'] = product.find('div', class_='listPrice').find_all('span', class_="ada-link")[1].get_text()
            item['sale_price'] = product.find('div', class_='salePrice').find_all('span', class_="ada-link")[1].get_text()
            if product.find('strong') is None:
                item['is_limited_sale'] = False
            else:
                item['is_limited_sale'] = True
            item['show_img'] = 'https:' + product.find('div', class_='product-image-container').find('img')['data-src']

            yield item


