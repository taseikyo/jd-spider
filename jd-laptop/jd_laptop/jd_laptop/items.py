# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdLaptopItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    product_id = scrapy.Field()
    price = scrapy.Field()
    shop_name = scrapy.Field()
    shop_id = scrapy.Field()
    comment = scrapy.Field()
    good_comment = scrapy.Field()
    good_rate = scrapy.Field()
    poor_comment = scrapy.Field()
    poor_rate = scrapy.Field()
