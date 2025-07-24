import scrapy
import csv
import os
from bricodepot_scraper.items import ProductItem  # adapte le chemin
import logging

class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['bricodepot.fr']

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['sku', 'title', 'url', 'price', 'category', 'subcategory', 'sub_subcategory'],
        'FEEDS': {
            'products1.csv': {
                'format': 'csv',
                'encoding': 'utf8',
            },
        }
    }

    def start_requests(self):
        path = 'categories.csv'
        if not os.path.exists(path):
            self.logger.error('categories.csv not found')
            return

        with open(path, newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['url']
                meta = {
                    'category': row.get('category', ''),
                    'subcategory': row.get('subcategory', ''),
                    'sub_subcategory': row.get('sub_subcategory', ''),
                }
                yield scrapy.Request(url=url, callback=self.reach_page_product, meta=meta)

    def reach_page_product(self, response):
        logging.warning("this is resposne meta", response.meta.get('category'))
        meta = {
                    'category': response.meta.get('category'),
                    'subcategory': response.meta.get('subcategory'),
                    'sub_subcategory': response.meta.get('sub_subcategory')
                }
        links = response.css('div.bd-ProductsListItem-link::attr(data-href)').getall()

        for link in links:
                yield response.follow(link, self.parse_products, meta=meta)

    
    def parse_products(self, response):
        product_blocks = response.css('div.bd-Container')

        for block in product_blocks:
            sku = block.css('span.bd-ProductDetails-tableDesc::text').get()

            product_url = response.url

            title = block.css('h1.bd-ProductCard-title span::text').get()
            title = title.strip() if title else None

            price_main = block.css('div.bd-price-container span::text').get()
            price_sup = block.css('div.bd-price-container sup::text').get()
            price = f"{price_main}{price_sup}".strip() if price_main else None

            item = ProductItem(
                sku=sku,
                title=title,
                url=product_url,
                price=price,
                category=response.meta.get('category'),
                subcategory=response.meta.get('subcategory'),
                sub_subcategory=response.meta.get('sub_subcategory'),
            )

            yield item

        # Pagination
        total = response.css('div.bd-ProductsList::attr(data-total-count)').get()
        total = int(total) if total else None
        current_page = int(response.css('div.bd-Products::attr(data-page-num)').get(default='1'))
        page_size = int(response.css('div.bd-Products::attr(data-page-size)').get(default='50'))

        if total and current_page * page_size < total:
            next_page = current_page + 1
            next_url = response.url.split('?')[0] + f'?page={next_page}'
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_products,
                meta=response.meta
            )
