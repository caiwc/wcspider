from base.crawl_async import Spider

class jianshu(Spider):
    url_list = ()
    headers = {}
    http_type = "html"

    def parser(self, data, resp):
        pass

