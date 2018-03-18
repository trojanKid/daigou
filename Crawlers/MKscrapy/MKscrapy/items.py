# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MkscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MKSaleProductItem(scrapy.Item):
    # 所欲获取的mk包包打折信息
    style_id = Field()  # style#:款号
    product_name = Field()  # 商品名
    details_url = Field()  # 商品详细信息页的url
    list_price = Field()  # 原价
    sale_price = Field()  # 折后价（不含税）
    is_limited_sale = Field()  # 是否是限时折扣,True是False否
    show_img = Field()  # 展示图对应的url


