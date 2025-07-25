# Scrapy
Projet pour l'ecole Simplon de découverte de Scrapy.

Ce projet Scrapy a pour but de réaliser un scraping de la concurrence pour BricoSimplon.

## Avertissement (Disclaimer)
Ce dépôt est fourni à des fins exclusivement pédagogiques dans le cadre de mon apprentissage en data engineering.
Aucune donnée scrappée n’est publiée dans ce dépôt (ni brute, ni agrégée).

- Je ne suis affilié à aucune des boutiques ou sites mentionnés.
- Les scripts ont été écrits pour démontrer des compétences techniques (requests, parsing, orchestration, stockage, etc.).
- Toute personne qui utiliserait ces scripts est seule responsable du respect :
    - des Conditions Générales d’Utilisation (CGU) et mentions légales des sites ciblés ;
    - des fichiers robots.txt ;
    - du RGPD et, plus largement, des lois applicables en matière de protection des données personnelles ;
    - du droit sui generis des bases de données (Code de la propriété intellectuelle, art. L341-1 s.) et de toute autre règle relative à l’extraction/réutilisation de données.
- Ces scripts ne doivent pas être utilisés pour contourner des mesures techniques de protection, des paywalls, ni pour réaliser une extraction substantielle ou réutilisation non autorisée de bases de données.
- Sur simple demande documentée d’un ayant droit, je m’engage à retirer ou modifier tout contenu problématique.

Contact retrait / takedown : ouvrir une issue sur ce dépôt ou me contacter à l'adresse reynier.aurore@gmail.com
Politique de retrait
Si vous estimez que ce dépôt porte atteinte à vos droits (ex. violation de CGU, extraction substantielle de base de données, atteinte à la vie privée), merci de :

1. Décrire précisément le contenu en cause (fichiers, lignes, commit).
2. Indiquer la base légale ou contractuelle invoquée.
3. Proposer la mesure attendue (suppression, modification, ajout de mention).

J’examinerai la demande de bonne foi et procéderai rapidement aux ajustements nécessaires.

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

2. Se déplacer dans le dossier bricodepot_scraper

3. Récupérer les catégories via un crawl ou le runner:
```
python3 runner.py
```

4. Récupérer les produits:
```
scrapy crawl products -o products.csv
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
    - **sub_subcategory**: sous sous-catégorie du produit
    - **sku**: référence unique du produit