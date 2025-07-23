import scrapy
from ..items import ProductItem
import json

class ProductSpider(scrapy.Spider):
    name = 'product_spider'

    def start_requests(self):
        with open('categories.json') as f:
            for cat in json.load(f):
                if cat.get('has_products') == 1:
                    yield scrapy.Request(cat['url'], meta={'category_slug': cat['slug']})

    def parse(self, response):
        slug = response.meta['category_slug']
        for href in response.css('a.product-item-link::attr(href)').getall():
            yield response.follow(href, self.parse_product, meta={'category_slug': slug})

    def parse_product(self, response):
        slug = response.url.rstrip('/').split('/')[-1]
        yield ProductItem(
            product_slug=slug,
            url=response.url,
            name=response.css('h1::text').get(default='').strip(),
            price=response.css('span.product-price::text').get(default='').strip(),
            image=response.css('img.main-image::attr(src)').get(default=''),
            category_slug=response.meta['category_slug']
        )
