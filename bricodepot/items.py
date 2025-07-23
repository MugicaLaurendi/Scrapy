# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CategoryItem(scrapy.Item):
    level = scrapy.Field()         # "category" ou "subcategory"
    slug = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    parent_url = scrapy.Field()
    has_products = scrapy.Field()  # 0 ou 1

class ProductItem(scrapy.Item):
    product_slug = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    category_slug = scrapy.Field()
