from base.crawl_async import Spider
from urllib.parse import urljoin
from bs4 import BeautifulSoup as BS
from item import JianshuItem
import re


class jianshu(Spider):
    item_header = {
        "Host": "www.jianshu.com",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Referer": "http://www.jianshu.com",
        "Accept - Encoding": "gzip, deflate",
        "Accept - Language": "zh-CN,zh;q=0.8",
    }

    url_list = [
        {"url": "http://www.jianshu.com/search/do?q=ldap&type=note&page=6&order_by=default"},
    ]
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

    http_type = "json"

    def parser(self, data, resp):
        print(self.queue.empty())
        u = resp.url.path_qs
        if not data:
            return

        if re.match("(.*?search/do\?q=ldap.*?)", u):
            page = data['page']
            if int(page) > 10:
                return

            self.put_url(
                {"url": "http://www.jianshu.com/search/do?q=ldap&type=note&page={0}&order_by=default".format(page + 1)})
            for item in data["entries"]:
                self.put_url({"url": "http://www.jianshu.com/p/{}".format(item['slug']), "http_type": "http",
                              "headers": self.item_header})
            return

        elif re.match("(.*?p/.*?)", u):
            soup = BS(data, "html.parser")
            JI = JianshuItem()
            JI.set("title", soup.find_all('h1',{'class':'title'}))
            print('hahaha')
            return JI
        else:
            pass
