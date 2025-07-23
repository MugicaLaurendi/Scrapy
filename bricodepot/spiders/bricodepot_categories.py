import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

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
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=(r'/catalogue/(amenagement-despaces|construction-renovation|outillage-quincaillerie)/.+/.+/$'),
                deny=(r'/\d+/', r'\?', r'/depot/', r'/prix-'),
            ),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        url = response.url
        name = response.css('h1::text').get(default='').strip()
        parent, slug = self.compute_parent_url_and_slug(url)

        # Détecte si la page liste des produits (présence de liens produits)
        prod_links = response.css('div.bd-Products').getall()
        has_products = 1 if prod_links else 0

        level = 'category' if url.count('/') - 3 == 2 else 'subcategory'
        yield {
            'level': level,
            'slug': slug,
            'url': url,
            'name': name,
            'parent_url': parent,
            'has_products': has_products
        }

    @staticmethod
    def compute_parent_url_and_slug(url):
        parts = url.rstrip('/').split('/')
        parent = '/'.join(parts[:-1]) + '/' if len(parts) > 1 else None
        slug = parts[-1]
        return parent, slug
