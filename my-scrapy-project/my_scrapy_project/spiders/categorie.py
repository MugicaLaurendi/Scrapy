import scrapy
from my_scrapy_project.items import CategorieItem

class CategoriesSpider(scrapy.Spider):
    # Nom unique du spider utilisé pour l'exécuter avec Scrapy
    name = "bricodepot_categories"
    # URL de départ pour le spider
    start_urls = ['https://www.bricodepot.fr/']

    def parse(self, response):
        # Sélectionne tous les éléments HTML correspondant aux sous-catégories
        links = response.css('li.bd-Submenu-item')

        for a in links:
            # Vérifie si l'élément a une classe spécifique indiquant qu'il s'agit d'une sous-catégorie
            if a.attrib['class'] == "bd-Submenu-item bd-Submenu-item--subitem":
                # Récupère le nom de la sous-catégorie
                name = a.css('a.bd-Submenu-link span::text').get()
                if not name:
                    continue  # Ignore si le nom est absent
                name = name.strip()  # Supprime les espaces inutiles

                # Récupère l'URL de la sous-catégorie
                url = a.css('a.bd-Submenu-link::attr(href)').get()
                if not url:
                    continue  # Ignore si l'URL est absente
                url = response.urljoin(url)  # Convertit l'URL relative en URL absolue

                # Récupère l'identifiant de la sous-catégorie à partir de l'URL
                id = url.split('/')[-2]

                # Récupère l'identifiant du parent à partir de l'URL
                parent = url.split('/')[-3]

                # Retourne les données sous forme d'objet CategorieItem
                yield CategorieItem(nom=name, url=url, id=id, parent=parent)
