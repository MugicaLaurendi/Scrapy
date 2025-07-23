import scrapy
from urllib.parse import urlparse
from bricodepot_scraper.items import CategoryItem, ProductItem

class BricodepotSpider(scrapy.Spider):
    name = 'bricodepot'
    allowed_domains = ['bricodepot.fr']
    start_urls = ['https://www.bricodepot.fr/']

    def extract_slug(self, url):
        path = urlparse(url).path
        slug = path.strip('/').split('/')[-1]
        return slug

    def parse(self, response):
        links = response.css('a.bd-MenuLink-link')

        for a in links:
            name = a.css('p.bd-MenuLink-displayName::text').get()
            if not name:
                continue

            url_relative = a.css('span.bd-MenuLink-label::attr(data-href)').get()
            if not url_relative:
                continue

            url = response.urljoin(url_relative)
            slug = self.extract_slug(url)

            yield scrapy.Request(
                url=url,
                callback=self.parse_subcategories,
                meta={'category_name': name.strip(), 'category_url': url, 'category_slug': slug}
            )

    def parse_subcategories(self, response):
        blocks = response.css('div.bd-CategoryItem.jsbd-gtm-clickUniverseSubCategory')

        if not blocks:
            # No sub-categories, go directly to products
            yield from self.parse_products(response)
            return

        for block in blocks:
            link = block.css('a.bd-CategoryItem-link')
            sub_url = link.attrib.get('href') if link else None
            sub_url = response.urljoin(sub_url) if sub_url else None

            sub_name = block.css('h3.bd-CategoryItem-name::text').get()
            sub_name = sub_name.strip() if sub_name else None

            if sub_name and sub_url:
                sub_slug = self.extract_slug(sub_url)
                subcategory = {
                    'name': sub_name,
                    'url': sub_url,
                    'slug': sub_slug
                }

                yield scrapy.Request(
                    url=sub_url,
                    callback=self.parse_subcategories,  # Recursively go deeper
                    meta={**response.meta, 'subcategory': subcategory}
                )

    def parse_products(self, response):
        # Get total number of products and current page
        total = response.css('div.bd-ProductsList::attr(data-total-count)').get()
        total = int(total) if total else None
        current_page = int(response.css('div.bd-Products::attr(data-page-num)').get(default='1'))
        page_size = int(response.css('div.bd-Products::attr(data-page-size)').get(default='50'))

        # Extract all product blocks
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
                'category': response.meta.get('category_name'),
                'subcategory': response.meta.get('subcategory', {}).get('name'),
            }

        # Pagination: get next page if needed
        if total and current_page * page_size < total:
            next_page = current_page + 1
            next_url = response.url.split('?')[0] + f'?page={next_page}'
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_products,
                meta=response.meta
            )

    def parse_subsubcategories(self, response):
        # Use parse_products directly instead of saving subsubcategories
        yield from self.parse_products(response)









