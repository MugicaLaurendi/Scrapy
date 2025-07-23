# Scrapy settings for my_scrapy_project

BOT_NAME = 'my_scrapy_project'

SPIDER_MODULES = ['my_scrapy_project.spiders']
NEWSPIDER_MODULE = 'my_scrapy_project.spiders'

# User agent
USER_AGENT = 'my_scrapy_project (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 0.1

AUTOTHROTTLE = True

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Enable or disable extensions
# EXTENSIONS = {
#     'scrapy.extensions.telnet.Telephone': None,
# }

# Enable or disable downloader middlewares
# DOWNLOADER_MIDDLEWARES = {
#     'my_scrapy_project.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#     'my_scrapy_project.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable item pipelines
# ITEM_PIPELINES = {
#     'my_scrapy_project.pipelines.MyCustomPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

