import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import CategoryItem

class BricoHierarchySpider(CrawlSpider):
    name = 'brico_hierarchy'
    allowed_domains = ['bricodepot.fr']
    start_urls = ['https://www.bricodepot.fr/']

    rules = (
        Rule(
            LinkExtractor(
                allow=(r'/catalogue/(amenagement-despaces|construction-renovation|outillage-quincaillerie)/[^/]+/$'),
                deny=(r'/\d+/', r'\?', r'/depot/', r'/prix-'),
            ),
            callback='parse_item',
            follow=True,
        ),
        Rule(
            LinkExtractor(
                allow=(r'/catalogue/(amenagement-despaces|construction-renovation|outillage-quincaillerie)/.+/.+/$'),
                deny=(r'/\d+/', r'\?', r'/depot/', r'/prix-'),
            ),
            callback='parse_item',
            follow=True,
        ),
    )

    def parse_item(self, response):
        url = response.url
        name = response.css('h1::text').get(default='').strip()
        parent, slug = self.compute_parent_and_slug(url)
        prod_links = response.css('a.product-item-link::attr(href)').getall()
        featured = response.css('div.bd.category-itemlink a::attr(href)').getall()
        real = [l for l in prod_links if l not in featured]
        has_products = 1 if real else 0
        level = 'category' if url.count('/') - 3 == 2 else 'subcategory'

        yield CategoryItem(
            level=level,
            slug=slug,
            url=url,
            name=name,
            parent_url=parent,
            has_products=has_products
        )

    @staticmethod
    def compute_parent_and_slug(url):
        parts = url.rstrip('/').split('/')
        slug = parts[-1]
        parent = '/'.join(parts[:-1]) + '/' if len(parts) > 1 else None
        return parent, slug
