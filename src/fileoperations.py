import pandas as pd
from crawler.url import URL

ATTRIBUTE_AMOUNT = 6
URL_IDENTIFIER = 'url'
URL_IDX = 6

CID_IDENTIFIER = 'cid'


class CSVOperations:
    def __init__(self, csvFile):
        self.df = pd.read_csv(csvFile, sep='\t')
        self.urls = self.df[URL_IDENTIFIER]

    def get_urls(self):
        return self.urls

    def get_cid_url_tuple(self):
        urls = []
        for index, row in self.df.iterrows():
            urls.append(URL(row[CID_IDENTIFIER],row[URL_IDENTIFIER]))
        return urls

    def get_url_for_cid(self, cid):
        rows = self.df[self.df[CID_IDENTIFIER] == cid].index.tolist()
        if len(rows):
            return self.df.loc[rows[0]][URL_IDENTIFIER]
        return None
