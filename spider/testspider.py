from crawl.base import Spider

class testspider(Spider):
    url_list = [1,2,4,5,23,54,23]


if __name__ == '__main__':
    testspider.run()