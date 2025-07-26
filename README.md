# Scrapy
Projet de découverte de Scrapy développé dans le cadre d'une formation en data engineering chez Simplon.

Ce projet Scrapy a pour but de réaliser scraping de la concurrence pour **BricoSimplon**.

## Avertissement (Disclaimer)
Ce dépôt est fourni à des fins exclusivement pédagogiques dans le cadre de notre apprentissage en data engineering.
Aucune donnée scrappée n’est publiée dans ce dépôt (ni brute, ni agrégée).

- Nous ne sommes affilié à aucune des boutiques ou sites mentionnés.
- Les scripts ont été écrits pour démontrer des compétences techniques (requests, parsing, orchestration, stockage, etc.).
- Toute personne qui utiliserait ces scripts est seule responsable du respect :
    - des Conditions Générales d’Utilisation (CGU) et mentions légales des sites ciblés ;
    - des fichiers robots.txt ;
    - du RGPD et, plus largement, des lois applicables en matière de protection des données personnelles ;
    - du droit sui generis des bases de données (Code de la propriété intellectuelle, art. L341-1 s.) et de toute autre règle relative à l’extraction/réutilisation de données.
- Ces scripts ne doivent pas être utilisés pour contourner des mesures techniques de protection, des paywalls, ni pour réaliser une extraction substantielle ou réutilisation non autorisée de bases de données.
- Sur simple demande documentée d’un ayant droit, nous nous engageons à retirer ou modifier tout contenu problématique.

Contact retrait / takedown : ouvrir une issue sur ce dépôt ou me contacter à l'adresse reynier.aurore@gmail.com

### Politique de retrait
Si vous estimez que ce dépôt porte atteinte à vos droits (ex. violation de CGU, extraction substantielle de base de données, atteinte à la vie privée), merci de :

1. Décrire précisément le contenu en cause (fichiers, lignes, commit).
2. Indiquer la base légale ou contractuelle invoquée.
3. Proposer la mesure attendue (suppression, modification, ajout de mention).

Nous examinerons la demande de bonne foi et procéderons rapidement aux ajustements nécessaires.

## Description
Notre script se base sur le scénario suivant:

*"En tant que Data Engineers au sein d'une start-up spécialisée dans la veille concurrentielle, nous jouons un rôle clé dans la collecte et l'analyse des données du marché. Notre entreprise utilise des techniques avancées de scraping pour extraire des informations pertinentes qui aideront nos clients à prendre des décisions stratégiques éclairées.*

*Notre nouveau client, **BricoSimplon**, est un grand site de e-commerce spécialisé dans le bricolage et l'aménagement de la maison. Face à une concurrence accrue, BricoSimplon souhaite optimiser sa politique tarifaire pour rester compétitif et fidéliser sa clientèle. Pour ce faire, ils ont besoin de connaître en temps réel les tarifs pratiqués par leurs principaux concurrents.*

*BricoSimplon nous a fourni une liste de magasins concurrents, tels que Castorama, Mano-mano, et Saint-Maclou, qu'ils souhaitent surveiller. Nous avons choisi l'un d'entre eux puis réalisé un script Scrapy afin de pouvoir extraire les données dont BricoSimplon a besoin pour sa veille concurrencielle."*

## Comment lancer le projet
Ce projet fonctionne sous Python v3.12.3 et Scrapy v2.13.3

1. Ajouter le fichier scrapy.cfg fourni à la racine du projet 

2. Installer les dépendances:
```
pip install -r requirements.txt
```

3. Se déplacer dans le dossier bricodepot_scraper
```
cd bricodepot_scraper
```

4. Récupérer les catégories via un crawl ou le runner:
```
python3 runner.py
```

5. Récupérer les produits:
```
scrapy crawl products -o products.csv
```

## Fonctionnalités
Ce projet scrapy récupère les données des catégories et des produits d'un concurrent direct de BricoSimplon.

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

## Choix techniques et limitations
Le site choisi étant conséquent, nous devions être vigilants concernant le rythme de nos requêtes afin de ne pas surcharger le site. nous avons notamment ajouté la commande `AUTOTHROTTLE_ENABLED = True` pour ralentir le scraping si le serveur ciblé a des difficultés à soutenir nos requêtes afin de ne pas le surcharger. Nous respectons également le fichier robots.txt du site visé.

Nous avons établi pour stratégie de récupérer les catégories en premier avec leurs URLs. Cela nous permet d'exploiter ces URLs pour la récupération des produits de façon optimisée pour récupérer chaque produit. Notre script est en mesure de récupérer tant les produits issus de listes ne comportant qu'une page que des produits issus de listes composées de plusieurs pages.

Notre pipeline nous sert à éliminer les doublons et convertir les prix en float afin d'avoir un format plus facilement exploitable.

Le site étant bien organisé et ne contenant pas de JavaScript, Scrapy seul a suffit pour atteindre l'objectif.

De même, la structure du site fait que si il y a ajout de nouvelles catégories et sous-catégories ou de nouveaux produits, notre script fonctionnera toujours pour ce site. Cependant, si le site est modifié de manière à avoir une structure radicalement différente, il faudrait probablement réfléchir à un script différent de celui-ci

Nous avons exporté les catégories et produits dans des fichiers CSV.