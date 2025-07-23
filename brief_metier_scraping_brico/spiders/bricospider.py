import scrapy
from brief_metier_scraping_brico.items import ProductItem


class BricospiderSpider(scrapy.Spider):
    name = "bricospider"
    allowed_domains = ["bricodepot.fr"]
    start_urls = ["https://www.bricodepot.fr"]

    def parse(self, response):
        categories = response.css('ul.bd-FooterLinks-list')
        if not categories:
            return

        product_categories = categories[0].css('li.bd-FooterLinks-listItem')
        
        for product_category in product_categories:
            brico_url = 'https://www.bricodepot.fr'
            splitted_url = product_category.css('a.bd-FooterLinks-link::attr(href)').get().split("/")
            reduced_url = splitted_url[0:3]
            joined_url = brico_url + "/".join(reduced_url)
            yield scrapy.Request(joined_url, callback=self.reach_products_categories)

    def reach_products_categories(self, response):
        if response.css('h1.bd-CategoryBanner-title--univers').get() is not None:            
            sub_categories = response.css('div.bd-CategoryItem')
            for sub_category in sub_categories:
                brico_url = 'https://www.bricodepot.fr'
            
                if sub_category.css('h3.bd-CategoryItem-name::text').get() is not None:
                    sub_category_link = brico_url + sub_category.css('a.bd-CategoryItem-link::attr(href)').get()
                    yield scrapy.Request(sub_category_link, callback=self.reach_products_categories)
        elif response.css('div.bd-ProductsListItem-box').get() is not None:
            tilings = response.css('div.bd-ProductsListItem-box')
            for tiling in tilings:
                brico_url = 'https://www.bricodepot.fr'
                relative_url = tiling.css('a.bd-ProductsListItem-top--link::attr(href)').get()
                product_url = brico_url + relative_url
                yield scrapy.Request(product_url, callback=self.parse_product_page)

            next_page = response.css('a.bd-Paging-link::attr(href)').get()
            if next_page is not None:
                next_page_url = 'https://www.bricodepot.fr' + next_page
                yield response.follow(next_page_url, callback=self.parse_product_category)
        else:
            self.logger.warning(f"Structure non reconnue pour l’URL : {response.url}")


    def parse_product_category(self, response):
        tilings = response.css('div.bd-ProductsListItem-box')
        for tiling in tilings:
            brico_url = 'https://www.bricodepot.fr'
            relative_url = tiling.css('a.bd-ProductsListItem-top--link::attr(href)').get()
            product_url = brico_url + relative_url
            yield scrapy.Request(product_url, callback=self.parse_product_page)

        next_page = response.css('a.bd-Paging-link::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.bricodepot.fr' + next_page
            yield response.follow(next_page_url, callback=self.parse_product_category)

    def parse_product_page(self, response):
        tiling = response.css('div.bd-Container')
        product_item = ProductItem()
        product_item['name'] = tiling.css('h1.bd-ProductCard-title span::text').get()
        product_item['price'] = tiling.css('div.bd-price-container span::text').get() + tiling.css('div.bd-price-container sup::text').get()
        product_item['url'] = response.url
        product_item['sku'] = tiling.css('span.bd-ProductDetails-tableDesc::text').get()
        yield product_item
