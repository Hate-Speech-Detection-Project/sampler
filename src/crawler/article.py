
class Article:
    XPATH_ARTICLE_HEADING = '//*[@id="js-article"]/header/div[1]/h1/span[3]'
    XPATH_RESSORT = '//*[@id="navigation"]/nav[3]/ul/li[1]/a/span'
    XPATH_ARTICLE_BODY = '//*[@id="js-article"]/div'
    XPATH_ARTICLE_HEAD = '/html/head'

    def __init__(self):
        self.corresponding_cid = ""
        self.text_body = ""
        self.heading = ""
        self.ressort = ""

    def set_corresponding_cid(self,cid):
        self.corresponding_cid = cid

    def get_corresponding_cid(self):
        return self.corresponding_cid

    def set_heading(self, heading):
        self.heading = heading

    def set_body(self, body):
        self.text_body = body

    def set_ressort(self, ressort):
        self.ressort = ressort

    def get_body(self):
        return self.text_body

    def get_heading(self):
        return self.heading

    def get_ressort(self):
        return self.ressort
