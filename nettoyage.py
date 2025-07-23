import csv

def remove_duplicate_products_by_url(input_file, output_file):
    seen_urls = set()
    unique_products = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get('url')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_products.append(row)

    # Écrire le CSV nettoyé
    if unique_products:
        fieldnames = unique_products[0].keys()  # Garde les mêmes colonnes
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_products)

    print(f"Nettoyage terminé : {len(unique_products)} produits uniques enregistrés dans {output_file}")


# Exemple d'utilisation
if __name__ == '__main__':
    remove_duplicate_products_by_url('products.csv', 'products_cleaned.csv')
