BOT_NAME = "bricodepot_scraper"

SPIDER_MODULES = ["bricodepot_scraper.spiders"]
NEWSPIDER_MODULE = "bricodepot_scraper.spiders"

ROBOTSTXT_OBEY = True


FEED_EXPORT_ENCODING = 'utf-8'
FEEDS = {
    'categories.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'fields': ['category', 'subcategory', 'url', 'slug'],
    },
}

