import pandas as pd
from crawler.url import URL

ATTRIBUTE_AMOUNT = 6
URL_IDENTIFIER = 'url'
URL_IDX = 5

CID_IDENTIFIER = 'cid'
CID_IDX = 0

class CSVOperations:
    def __init__(self, csvFile):
        self.df = pd.read_csv(csvFile, sep=',')
        urlColumn = self.df[self.df.columns[URL_IDX]]
        urls = []
        id = 0
        for url in set(urlColumn):
            urls.append(URL(id, url))
            id = id +1
        self.urls = urls

    def get_urls(self):
        return self.urls

    def get_url_for_cid(self, cid):
        for url in self.urls:
            if url.get_cid() == cid:
                return url.get_url()
        return None
