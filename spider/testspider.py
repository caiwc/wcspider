from base.crawl_async import Spider
from item import TestItem

class testspider(Spider):
    url_list = (1, 55, 4, 5, 23, 54, 6, 54, 54, 4)
    headers = {'content-type': 'application/json'}
    http_type = "json"

    def parser(self, data, resp):
        i = TestItem()
        i.set('name',data["origin"])
        i.set('num',data["args"]["a"])
        i.set('url',data['url'])

        num = i.get('num')
        if int(num) % 3 == 0:
            self.put_url(int(num) + 1)
        print(resp.url)
        return i


if __name__ == '__main__':
    import time
    now = time.time()
    s = testspider()
    s.run()
    print(s.result.__len__(),time.time()-now)
    print(s.seen.seen_url)