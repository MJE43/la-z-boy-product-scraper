import scrapy


class LzbItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    saleprice = scrapy.Field()
    description = scrapy.Field()
    features = scrapy.Field()
    pitch = scrapy.Field()
    stylenumber = scrapy.Field()
    image = scrapy.Field()
    pass
