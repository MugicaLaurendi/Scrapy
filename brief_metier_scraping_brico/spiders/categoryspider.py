import scrapy
from brief_metier_scraping_brico.items import CategoryItem

class CategoryspiderSpider(scrapy.Spider):
    name = "categoryspider"
    allowed_domains = ["bricodepot.fr"]
    start_urls = ["https://bricodepot.fr"]

    def parse(self, response):
        categories = response.css('ul.bd-FooterLinks-list')
        product_categories = categories[0].css('li.bd-FooterLinks-listItem')
        for product_category in product_categories:
            brico_url = 'https://www.bricodepot.fr'
            splitted_url = product_category.css('a.bd-FooterLinks-link::attr(href)').get().split("/")
            reduced_url = splitted_url[0:3]
            joined_url = brico_url + "/".join(reduced_url)
            yield scrapy.Request(joined_url, callback=self.parse_category)



    def parse_category(self, response):
        splitted_url = response.url.split("/")
        reduced_url = splitted_url[-1]
        joined_url = "".join(reduced_url)
        if response.css('h1.bd-CategoryBanner-title--univers').get() is not None:            
            category_item = CategoryItem()
            category_item['id'] = joined_url,
            category_item['name'] = response.css('h1.bd-CategoryBanner-title--univers::text').get()
            category_item['url'] = response.url,
            yield category_item


            sub_categories = response.css('div.bd-CategoryItem')
            for sub_category in sub_categories:
                splitted_url = sub_category.css('a.bd-CategoryItem-link::attr(href)').get().split("/")
                reduced_url = splitted_url[-2]
                joined_url = "".join(reduced_url)

                brico_url = 'https://www.bricodepot.fr'
            
                if sub_category.css('h3.bd-CategoryItem-name::text').get() is not None:
                    category_item = CategoryItem()
                    category_item['id'] = joined_url,
                    category_item['name'] =  sub_category.css('h3.bd-CategoryItem-name::text').get(),
                    category_item['url'] = brico_url + sub_category.css('a.bd-CategoryItem-link::attr(href)').get()
                    yield category_item

                    brico_url = 'https://www.bricodepot.fr'
                    sub_category_link = brico_url + sub_category.css('a.bd-CategoryItem-link::attr(href)').get()
                    yield scrapy.Request(sub_category_link, callback=self.parse_sub_category)


    def parse_sub_category(self, response):
        sub_categories = response.css('div.bd-CategoryItem')
        for sub_category in sub_categories:
            splitted_url = sub_category.css('a.bd-CategoryItem-link::attr(href)').get().split("/")
            reduced_url = splitted_url[-2]
            joined_url = "".join(reduced_url)

            brico_url = 'https://www.bricodepot.fr'
            
            if sub_category.css('h3.bd-CategoryItem-name::text').get() is not None:
                category_item = CategoryItem()
                category_item['id'] = joined_url,
                category_item['name'] =  sub_category.css('h3.bd-CategoryItem-name::text').get(),
                category_item['url'] = brico_url + sub_category.css('a.bd-CategoryItem-link::attr(href)').get()
                yield category_item

            if sub_category.css('a.bd-CategoryItem-link::attr(href)').get() is not None:
                sub_sub_category_link = brico_url + sub_category.css('a.bd-CategoryItem-link::attr(href)').get()
                yield scrapy.Request(sub_sub_category_link, callback=self.parse_sub_category)
