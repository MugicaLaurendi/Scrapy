import scrapy

class CategorieItem(scrapy.Item):
    nom = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
    parent = scrapy.Field()

class PageListItem(scrapy.Item):
        nom = scrapy.Field()
        prix = scrapy.Field()
        url = scrapy.Field()
        sku = scrapy.Field()
        categorie = scrapy.Field()

