# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LenovoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # pass
    price = scrapy.Field()
    name = scrapy.Field()
    shopname = scrapy.Field()
    num_comment = scrapy.Field()
    item_id = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    GoodRate = scrapy.Field()
    DefaultGoodCount = scrapy.Field()
    PoorCount = scrapy.Field()
    PoorRate = scrapy.Field()
    GoodCount = scrapy.Field()