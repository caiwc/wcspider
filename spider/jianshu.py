from base.crawl_async import Spider
from urllib.parse import urljoin
from bs4 import BeautifulSoup as BS
from item import JianshuItem
import re
import datetime
import json

class jianshu(Spider):
    query = 'java'

    item_header = {
        "Host": "www.jianshu.com",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Referer": "http://www.jianshu.com/search?q={}&page=1&type=note".format(query),
        "Accept - Encoding": "gzip, deflate",
        "Accept - Language": "zh-CN,zh;q=0.8",
    }

    url_list = [
        {"url": "http://www.jianshu.com/search/do?q={}&type=note&page=1&order_by=default".format(query)},
    ]
    baser_url = "http://www.jianshu.com/"
    headers = {
        "Host": "www.jianshu.com",
        "Connection": "keep-alive",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Referer": "http://www.jianshu.com/search?q={}&page=1&type=note".format(query),
        "Accept - Encoding": "gzip, deflate",
        "Accept - Language": "zh-CN,zh;q=0.8",
    }

    http_type = "json"
    method = 'POST'

    def parser(self, data, resp):
        print(self.queue.empty())
        u = resp.url.path_qs
        if not data:
            return

        if re.match("(.*?search/do\?q={}.*?)".format(self.query), u):
            page = data['page']
            if int(page) > 20:
                return

            self.put_url(
                {"url": "http://www.jianshu.com/search/do?q={1}&type=note&page={0}&order_by=default".format(
                    page + 1, self.query),
                })
            for item in data["entries"]:
                self.put_url({"url": "http://www.jianshu.com/p/{}".format(item['slug']), "http_type": "http",
                              "headers": self.item_header, 'method': 'GET'})
            return

        elif re.match("(.*?p/.*?)", u):
            soup = BS(data, "html.parser")
            JI = JianshuItem()
            try:
                JI.set("title", soup.find_all('h1', {'class': 'title'})[0].text)
                JI.set("url", urljoin(self.baser_url, u))
                JI.set("content", soup.find('div', {'class': 'show-content'}).text)
                t = soup.find('span', {'class': 'publish-time'}).text
                JI.set("ctime", time_change(t))
                wordage = soup.find('span', {'class': 'wordage'})
                if wordage:
                    JI.set("wordage", num_change(wordage.text))
                data_json = soup.find("script",{"data-name":"page-data"})
                if data_json:
                    article_data_json = json.loads(data_json.text)['note']
                    JI.set("like",article_data_json.get('likes_count',0))
                    JI.set("comment", article_data_json.get('comments_count', 0))
                    JI.set("view", article_data_json.get('views_count', 0))
            except Exception as e:
                print("error", str(e) + '-' + urljoin(self.baser_url, u))
                return
            print('get a item')
            return JI
        else:
            pass


def time_change(t):
    return datetime.datetime.strptime(t.strip('*'), "%Y.%m.%d %H:%M")


def num_change(s):
    num_str = s.split(" ")[-1]
    try:
        return int(num_str)
    except:
        return 0
