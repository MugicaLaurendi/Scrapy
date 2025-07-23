import json

def remove_duplicate_products_by_url(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    seen_urls = set()
    unique_products = []

    for product in products:
        url = product.get('url')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_products.append(product)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_products, f, ensure_ascii=False, indent=4)

    print(f"Nettoyage terminé : {len(unique_products)} produits uniques enregistrés dans {output_file}")


# Exemple d'utilisation
if __name__ == '__main__':
    remove_duplicate_products_by_url('products.json', 'produits_uniques.json')
