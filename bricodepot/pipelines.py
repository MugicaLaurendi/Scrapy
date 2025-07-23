from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

class CleanValidateDedupPipeline:
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 1. Validation minimale
        url = adapter.get('url')
        slug = adapter.get('slug') or adapter.get('product_slug')
        if not url or not slug:
            raise DropItem(f"Missing url/slug in {item}")

        # 2. Nettoyage
        name = adapter.get('name')
        if name:
            adapter['name'] = name.strip()

        price = adapter.get('price')
        if price:
            try:
                adapter['price'] = float(price.replace('€', '').replace(',', '.').strip())
            except Exception:
                adapter['price'] = price  # ou adapter['price'] = None

        # 3. Déduplication
        unique_key = (slug, adapter.get('level') or 'product')
        if unique_key in self.seen:
            raise DropItem(f"Duplicate item {unique_key}")
        self.seen.add(unique_key)

        return item
