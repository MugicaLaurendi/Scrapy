import scrapy
from urllib.parse import urlparse
from bricodepot_scraper.items import CategoryItem  # adapte le chemin vers ton fichier items.py

class CategoriesSpider(scrapy.Spider):
    name = 'categories'
    allowed_domains = ['bricodepot.fr']
    start_urls = ['https://www.bricodepot.fr/']

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['category', 'subcategory', 'sub_subcategory', 'url', 'slug'],
        'FEEDS': {
            'categories.csv': {
                'format': 'csv',
                'encoding': 'utf8',
            },
        }
    }

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

            # Niveau 1
            item = CategoryItem(
                category=name.strip(),
                subcategory='',
                sub_subcategory='',
                url=url,
                slug=slug
            )
            yield item

            yield scrapy.Request(
                url=url,
                callback=self.parse_subcategories,
                meta={'category_name': name.strip()}
            )

    def parse_subcategories(self, response):
        blocks = response.css('div.bd-CategoryItem.jsbd-gtm-clickUniverseSubCategory')

        for block in blocks:
            link = block.css('a.bd-CategoryItem-link')
            sub_url = link.attrib.get('href') if link else None
            sub_url = response.urljoin(sub_url) if sub_url else None

            sub_name = block.css('h3.bd-CategoryItem-name::text').get()
            sub_name = sub_name.strip() if sub_name else None

            if sub_name and sub_url:
                sub_slug = self.extract_slug(sub_url)

                # Niveau 2
                item = CategoryItem(
                    category=response.meta['category_name'],
                    subcategory=sub_name,
                    sub_subcategory='',
                    url=sub_url,
                    slug=sub_slug
                )
                yield item

                yield scrapy.Request(
                    url=sub_url,
                    callback=self.parse_sub_subcategories,
                    meta={
                        'category_name': response.meta['category_name'],
                        'subcategory_name': sub_name
                    }
                )

    def parse_sub_subcategories(self, response):
        blocks = response.css('div.bd-CategoryItem.jsbd-gtm-clickUniverseSubCategory')
        self.logger.info(f"Found {len(blocks)} sub_subcategories in {response.url}")

        for block in blocks:
            link = block.css('a.bd-CategoryItem-link')
            sub_sub_url = link.attrib.get('href') if link else None
            sub_sub_url = response.urljoin(sub_sub_url) if sub_sub_url else None

            sub_sub_name = block.css('h3.bd-CategoryItem-name::text').get()
            sub_sub_name = sub_sub_name.strip() if sub_sub_name else None

            if sub_sub_name and sub_sub_url:
                sub_sub_slug = self.extract_slug(sub_sub_url)

                # Niveau 3
                item = CategoryItem(
                    category=response.meta['category_name'],
                    subcategory=response.meta['subcategory_name'],
                    sub_subcategory=sub_sub_name,
                    url=sub_sub_url,
                    slug=sub_sub_slug
                )
                yield item
