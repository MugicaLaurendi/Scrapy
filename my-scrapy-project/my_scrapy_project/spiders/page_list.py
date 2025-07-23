import scrapy
from my_scrapy_project.items import PageListItem


class PageListSpider(scrapy.Spider):
    
    name = "bricodepot_page_list"
    start_urls = ['https://www.bricodepot.fr/']

    def parse(self, response):

        # Extraction des liens des sous-catégories
        links = response.css('li.bd-Submenu-item')

        for a in links:

            if "bd-Submenu-item--subitem" in a.attrib.get('class', ''):
                nom_categorie = a.css('a.bd-Submenu-link span::text').get()
                if not nom_categorie:
                    continue
                nom_categorie = nom_categorie.strip()

                url = a.css('a.bd-Submenu-link::attr(href)').get()
                if not url:
                    continue
                url = response.urljoin(url)

                # Passer la catégorie au prochain parse
                yield response.follow(url, self.parse_page_list, meta={'categorie': nom_categorie})

    def parse_page_list(self, response):

        # Récupérer la catégorie depuis les meta
        categorie = response.meta.get('categorie', 'Inconnue')

        # Extraction des produits
        links = response.css('div.bd-ProductsListItem-link::attr(data-href)').getall()

        for url in links:

            yield response.follow(url, self.parse_product, meta={'categorie': categorie, 'url': url})


    def parse_product(self, response):

        # Récupérer les informations depuis les meta
        categorie = response.meta.get('categorie', 'Inconnue')
        url = response.meta.get('url', response.url)

        # Extraction des détails du produit
        sku = response.css('span.bd-ProductDetails-tableDesc::text').get()
        nom = response.css('h1.bd-ProductCard-title span::text').get()
        euro = response.css('div.bd-price-container span::text').get()
        centime = response.css('div.bd-price-container span sup::text').get()
        prix = euro + centime

        yield PageListItem(nom=nom, prix=prix, url=url, sku=sku, categorie=categorie)
