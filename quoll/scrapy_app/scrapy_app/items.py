# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Event(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    venue = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    artists = scrapy.Field()
