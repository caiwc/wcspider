from crawl.base import Spider


class testspider(Spider):
    url_list = [1, 2, 4, 5, 23, 54, 23, 6, 8, 9, 4]
    headers = {'content-type': 'application/json'}
    http_type = "json"

    def parser(self, data, resp):
        res = {
            "arg": data["args"]["a"],
            "origin": data["origin"],
            "url": data["url"],
            "yes": "lj"
        }
        num = data["args"]["a"]
        if int(num) % 3 == 0:
            self.put_url(str(int(num) + 1))
        print(resp.url)
        return res


if __name__ == '__main__':
    import time
    now = time.time()
    s = testspider()
    s.run()
    print(s.result.__len__(),time.time()-now)