import csv
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class EuroToFloatPipeline:

    def process_item(self, item, spider):
        price = item.get('price')
        if price and spider.name != 'categories':
            item['price'] = float(item['price'].replace('€','.'))

        return item
    
class RemoveDuplicatePipeline:

    def process_item(self, item, spider):

        self.ids_seen = set()

        #adapter = ItemAdapter(item)
        unique = item['url']
        #unique = adapter.get('url')

        if unique is None:
            # Pas de champ unique → on laisse passer
            return item

        if unique in self.ids_seen:
            raise DropItem(f"Duplicate item found: {unique}")
        
        self.ids_seen.add(unique)

        return item