# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserComment(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    partition = scrapy.Field()
    tm = scrapy.Field()
    no = scrapy.Field()
    amount = scrapy.Field()
    cash_type = scrapy.Field()
    comment = scrapy.Field()
    page = scrapy.Field()
    page_pos = scrapy.Field()



