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

        meta = {
                    'category': response.meta.get('category'),
                    'subcategory': response.meta.get('subcategory'),
                    'sub_subcategory': response.meta.get('sub_subcategory')
                }
        links = response.css('div.bd-ProductsListItem-link::attr(data-href)').getall()

        for link in links:
            yield response.follow(link, self.parse_products, meta=meta)

        
        url_nextpage = response.css('a.bd-Paging-link.bd-Icon.bd-Icon--sliderRight::attr(href)').get()
        print("NEXT PAGE ?", url_nextpage)
        current_page = response.css('a.bd-Paging-link.bd-Icon.bd-Icon--sliderRight::attr(data-num)').get()
        print(f"current_page : {current_page}")

        if url_nextpage :
            logging.info(" -------------------------- NEXT PAGE --------------------------------")
            url_nextpage = "https://www.bricodepot.fr" + url_nextpage
            yield scrapy.Request(url=url_nextpage, callback=self.reach_page_product, meta=response.meta)


    def parse_products(self, response):
        sku = response.css('span.bd-ProductDetails-tableDesc::text').get()

        product_url = response.url

        title = response.css('h1.bd-ProductCard-title span::text').get()
        title = title.strip() if title else None

        price_main = response.css('div.bd-price-container span::text').get()
        price_sup = response.css('div.bd-price-container sup::text').get()
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

