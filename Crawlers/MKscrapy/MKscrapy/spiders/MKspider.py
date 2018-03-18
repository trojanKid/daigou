import scrapy
import re
from bs4 import BeautifulSoup
from scrapy.http import Request

class MKspider(scrapy.Spider):
    name = 'MKspider'

    def start_requests(self):
        urls = [
            "https://www.michaelkors.com/sale/handbags/_/N-289z"
        ]
        for url in urls:
            yield Request(url, self.parse)

    def parse(self, response):
        # item = MyfirstscrapyItem()
        # authors = BeautifulSoup(response.text, 'lxml').find_all('small', itemprop='author')
        # quotes = BeautifulSoup(response.text, 'lxml').find_all('span', itemprop="text")
        # nums = len(authors)
        # for i in range(0, nums-1):
        #     item['author'] = authors[i].get_text()
        #     print(authors[i].get_text())
        #     item['quote'] = quotes[i].get_text()
        #     print(quotes[i].get_text())
        #     yield item
        bs = BeautifulSoup(response.text, 'lxml')
        # .find_all('div', class_='medium-12 row panel tile-listing')
        get_sale_count = bs.find('span', class_='product-count').contents[0]
        get_sale_count = int(get_sale_count)
        prices = bs.find_all('div', class_='salePrice')
        have_sale_count = len(prices)
        if have_sale_count == get_sale_count:
            print('Have gotten every product! Have:', have_sale_count, 'Get:', get_sale_count)
        else:
            print('Missing some products! Have:', have_sale_count, 'Get:', get_sale_count)
