import scrapy
import re
from crawler.article import Article
from w3lib.html import remove_tags, remove_tags_with_content

HTTP_RESPONSE_OK = 200
ID_IDENTIFIER = 'id'


class ArticelCrawler(scrapy.Spider):
    name = "article"
    allowed_domains = ["zeit.de"]
    handle_httpstatus_list = [404]
    urls = []
    articles = []
    failed_urls = []

    def start_requests(self):
        print('crawling....')
        for url in self.urls:
            if url.get_url() and type(url.get_url()) is str:
                yield scrapy.Request(url=url.get_url(), callback=self.parse, method='GET',
                                     meta={ID_IDENTIFIER: url.get_id()}, )

    def __init__(self):
        super().__init__(self)



    def parse(self, response):
        if response.status != HTTP_RESPONSE_OK:
            self.failed_urls.append([response.meta[ID_IDENTIFIER], response.status, response.url])
        else:
            self.articles.append(self._create_article_from_response(response))

    @staticmethod
    def get_failed_urls():
        return ArticelCrawler.failed_urls

    @staticmethod
    def get_articles():
        return ArticelCrawler.articles



    # creates an article based on the crawler-response
    def _create_article_from_response(self, response):
        article = Article()

        article.set_id(response.meta[ID_IDENTIFIER])

        heading = response.xpath(Article.XPATH_ARTICLE_HEADING).extract_first()
        if heading is not None:
            article.set_heading(self._filter_text_from_markup(heading))

        ressort = response.xpath(Article.XPATH_RESSORT).extract_first()
        if ressort is not None:
            article.set_ressort(self._filter_text_from_markup(ressort).lower())
        else:
            self._parse_html_head_and_set_ressort(response, article)

        article_body = response.xpath(Article.XPATH_ARTICLE_BODY).extract_first()
        if article_body is not None:
            article.set_body(self._filter_text_from_markup(article_body))
        return article

    # removes markup-tags from the given text
    def _filter_text_from_markup(self, markup):
        return remove_tags(remove_tags_with_content(markup, ('script',)))

    # parses the html-header in order to find ressorts in the scripts for the given article
    def _parse_html_head_and_set_ressort(self, response, article):
        header = response.xpath(Article.XPATH_ARTICLE_HEAD)[0].extract()
        # extracts all occurrences of 'ressort': "..."  or 'sub_ressort': "..." in the html-header in order
        # to get the ressort
        ressort = self._find_ressort_by_regex('\'ressort\': "(.+)"', header)
        if (ressort is None):
            ressort = self._find_ressort_by_regex('\'sub_ressort\': "(.+)"', header)

        # set the specific ressort
        article.set_ressort(ressort)

    def _find_ressort_by_regex(self, regex, text):
        ressortMatch = re.search(regex, text)
        ressort = None
        if ressortMatch is not None:
            # the string  'ressort': "politik"  is trimmed to politik
            ressort = re.search('"(.+)"', ressortMatch.group(0)).group(0).replace('"', '')
        return ressort
