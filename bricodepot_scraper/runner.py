import os
from scrapy.cmdline import execute

category_spider = "categories"
try:
    execute([
        'scrapy',
        'crawl',
        category_spider,
        '-o',
        f'{category_spider}.csv'
    ])
    
except SystemExit as e:
    print(f"\nError, exit script : {e}\n")
    pass