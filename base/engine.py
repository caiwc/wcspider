from importlib import import_module


def engine(spider_name):
    module = import_module("spider.%s" % spider_name)
    spider = getattr(module, spider_name)
    s = spider()
    s.run()
    print(s.result)

if __name__ == '__main__':
    engine("testspider")