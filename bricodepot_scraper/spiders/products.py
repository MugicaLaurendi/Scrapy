import scrapy
import csv
import os

class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['bricodepot.fr']
    custom_settings = {
        # Optionnel : changer output file
        'FEEDS': {
            'products.csv': {
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
                    'category': row['category'],
                    'subcategory': row['subcategory'],
                }
                yield scrapy.Request(url=url, callback=self.parse_products, meta=meta)

    def parse_products(self, response):
        product_blocks = response.css('div.bd-ProductsListItem')

        for block in product_blocks:
            product_url = block.css('div.bd-ProductsListItem-link::attr(data-href)').get()
            product_url = response.urljoin(product_url) if product_url else None

            title = block.css('h3.bd-ProductsListItem-title::text').get()
            title = title.strip() if title else None

            image = block.css('img.bd-ProductsListItem-picture::attr(src)').get()

            price_main = block.css('span.bd-Price-current::text').get()
            price_sup = block.css('sup.bd-Price-currentSup::text').get()
            price = f"{price_main}{price_sup}".strip() if price_main else None

            stock_text = block.css('div.bd-ProductsListItem-stock span::text').get()
            stock = stock_text.strip() if stock_text else None

            yield {
                'title': title,
                'url': product_url,
                'image': image,
                'price': price,
                'stock': stock,
                'category': response.meta.get('category'),
                'subcategory': response.meta.get('subcategory'),
            }

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
