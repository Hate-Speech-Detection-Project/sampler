from fileoperations import CSVOperations
from crawler.article_crawler import ArticelCrawler
from scrapy.crawler import CrawlerProcess

path = '../data/sample.csv'
csvFile = open(path, 'rU', encoding="utf8")

ops = CSVOperations(csvFile)

all_urls = ops.get_cid_url_tuple()

ArticelCrawler.urls.extend(all_urls)

# start the crawler
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_LEVEL': 'INFO'
})
process.crawl(ArticelCrawler)
process.start()  # the script will block here until the crawling is finished

print('failed URLs are:')
print(ArticelCrawler.get_failed_urls())

print('following articles could be created: ')
for article in ArticelCrawler.get_articles():
    print('cid: ' + article.get_corresponding_cid() + ', ressort: ' + article.get_ressort())
