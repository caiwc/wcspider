from importlib import import_module
from timeit import timeit

def engine(spider_name):
    module = import_module("spider.%s" % spider_name)
    spider = getattr(module, spider_name)
    s = spider()
    s.run()
    print(len(s.result))

if __name__ == '__main__':
    time = timeit("engine('jianshu')", setup="from __main__ import engine",number=1)
    print(time)