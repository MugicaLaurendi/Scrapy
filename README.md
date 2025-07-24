# Scrapy
Projet pour l'ecole Simplon de découverte de Scrapy.

Ce projet Scrapy a pour but de réaliser un scraping de la concurrence pour BricoSimplon.

## Description
En tant que Data Engineer au sein d'une start-up spécialisée dans la veille concurrentielle, vous jouez un rôle clé dans la collecte et l'analyse des données du marché. Votre entreprise utilise des techniques avancées de scraping pour extraire des informations pertinentes qui aideront vos clients à prendre des décisions stratégiques éclairées.

Votre nouveau client, **BricoSimplon**, est un grand site de e-commerce spécialisé dans le bricolage et l'aménagement de la maison. Face à une concurrence accrue, BricoSimplon souhaite optimiser sa politique tarifaire pour rester compétitif et fidéliser sa clientèle. Pour ce faire, ils ont besoin de connaître en temps réel les tarifs pratiqués par leurs principaux concurrents.

BricoSimplon vous fournit une liste de magasins concurrents, tels que Castorama, Mano-mano, et Saint-Maclou, qu'ils souhaitent surveiller. 

## Comment lancer le projet
Ce projet fonctionne sous Python v3.12.3 et Scrapy v2.13.3

1. Installer les dépendances:
```
pip install -r requirements.txt
```

2. Lancer le runner:
```
python3 runner.py
```

## Fonctionnalités
Ce projet scrapy récupère les données d'un concurrent direct de BricoSimplon.

Il est composé de deux spiders:
- **categories**: récupération de toutes les catégories et sous-catégories liées aux produits
- **products**: récupération de tous les produits

Les items associés:
- **categories**:
    - **name**: nom de la catégorie
    - **url**: url de la catégorie
    - **subcategories**: nom de la sous-catégorie 
    - **slug**: slug de la catégorie
    
- **products**:
    - **name**: nom du produit
    - **price**: prix du produit
    - **url**: url du produit
    - **category**: catégorie du produit
    - **subcategory**: sous-catégorie du produit
    - **sku**: référence unique du produit
    - **stock**: stock du produit