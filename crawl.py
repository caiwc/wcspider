import requests


class BaseSpider(object):
    def __init__(self, url, method):
        self.url = url
        self.method = method.upper()

    def __call__(self, *args, **kwargs):
        text = self.Crawl()
        self.Analyze(text)
        self.Save()

    def Crawl(self):
        print("crawling--"+self.url)
        res = requests.request(url=self.url, method=self.method)
        return res.text

    def Analyze(self,text):
        print("do analysis")
        pass

    def Save(self):
        print("do save")
        pass


if __name__ == '__main__':
    b =BaseSpider('https://www.baidu.com/','get')
    b.__call__()