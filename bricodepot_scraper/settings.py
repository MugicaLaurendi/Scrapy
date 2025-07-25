BOT_NAME = "bricodepot_scraper"

SPIDER_MODULES = ["bricodepot_scraper.spiders"]
NEWSPIDER_MODULE = "bricodepot_scraper.spiders"

ROBOTSTXT_OBEY = True


FEED_EXPORT_ENCODING = 'utf-8'

AUTOTHROTTLE_ENABLED = True

ITEM_PIPELINES = {
    'bricodepot_scraper.pipelines.RemoveDuplicatePipeline': 200,
    'bricodepot_scraper.pipelines.EuroToFloatPipeline': 300,
}