import scrapy

class CategoryItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    subcategories = scrapy.Field()
    slug = scrapy.Field()


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    # Ajoute d'autres champs selon ton besoin
    