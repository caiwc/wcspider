script = """from base.crawl_async import Spider

class %s(Spider):
    url_list = ()
    headers = {}
    http_type = "html"

    def parser(self, data, resp):
        pass

"""