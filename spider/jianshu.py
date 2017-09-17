from base.crawl_async import Spider
from urllib.parse import urljoin
from bs4 import BeautifulSoup as BS
import re


class jianshu(Spider):
    url_list = ["http://www.jianshu.com/search?q=python&page=1&type=note"]
    baser_url = "http://www.jianshu.com/"
    headers = {
        "Host": "www.jianshu.com",
        "Connection": "keep-alive",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Referer": "http://www.jianshu.com/search?q=python&page=1&type=note",
        "Accept - Encoding": "gzip, deflate",
        "Accept - Language": "zh-CN,zh;q=0.8",
    }
    http_type = "html"

    def parser(self, data, resp):
        u = resp.url.path_qs
        if re.match("(.*?/search\?q=python.*?)",u):
            print("12")
        elif re.match("(.*?p/.*?)",u):
            print("sada")
            soup = BS(data, "html.parser")
            item_url = soup.find_all("a", {"class": "title"})
            for item in item_url:
                url = urljoin(self.baser_url, item.get('href'))
                print(url)

            pages = soup.find_all("ul", {"class": "pagination"})

        return