import scrapy
from urllib.parse import urlparse
from bricodepot_scraper.items import CategoryItem

class CategoriesSpider(scrapy.Spider):
    name = 'categories'
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

            yield {
                'category': name.strip(),
                'subcategory': '',
                'url': url,
                'slug': slug
            }

            yield scrapy.Request(
                url=url,
                callback=self.parse_subcategories,
                meta={'category_name': name.strip(), 'category_url': url, 'category_slug': slug}
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
                yield {
                    'category': response.meta['category_name'],
                    'subcategory': sub_name,
                    'url': sub_url,
                    'slug': sub_slug
                }

                yield scrapy.Request(
                    url=sub_url,
                    callback=self.parse_subcategories,  # récursif
                    meta={'category_name': response.meta['category_name']}
                )
