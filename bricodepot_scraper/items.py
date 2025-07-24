import scrapy

class CategoryItem(scrapy.Item):
    category = scrapy.Field()        
    subcategory = scrapy.Field()     
    sub_subcategory = scrapy.Field() 
    url = scrapy.Field()
    slug = scrapy.Field()


class ProductItem(scrapy.Item):
    sku = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    sub_subcategory = scrapy.Field()
    