from fileoperations import CSVOperations
from crawler.article_crawler import ArticelCrawler
from scrapy.crawler import CrawlerProcess
from db_interface import DBInterface
from crawler.url import URL

import sys
from pathlib import Path


if sys.argv[1] and Path(sys.argv[1]).is_file():
    path = sys.argv[1]
    csvFile = open(path, 'rU', encoding="utf8")
else:
    print('Path is not correct or it is not a file')
    sys.exit()

# insert crawled articles into the db
dbInterface = DBInterface()
if not dbInterface.article_table_already_exists():
    print('Created Table articles')
    dbInterface.create_articles_table()

ops = CSVOperations(csvFile)
ArticelCrawler.urls.extend(ops.get_urls())

# start the crawler
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(ArticelCrawler)
process.start()  # the script will block here until the crawling is finished

print('failed URLs are:')
print(ArticelCrawler.get_failed_urls())

