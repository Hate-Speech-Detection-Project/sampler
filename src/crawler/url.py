
class URL:

    def __init__(self, id, url):
        self.url = url
        self.id = id


    def get_url(self):
        return self.url

    def get_id(self):
        return self.id

    def set_url(self,url):
        self.url = url

    def set_id(self,id):
        self.id = id

