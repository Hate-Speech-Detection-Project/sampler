
class URL:

    def __init__(self, cid, url):
        self.url = url
        self.cid = cid


    def get_url(self):
        return self.url

    def get_cid(self):
        return self.cid

    def set_url(self,url):
        self.url = url

    def set_cid(self,cid):
        self.cid = cid

