from importlib import import_module
import timeit


def engine(spider_name):
    module = import_module("spider.%s" % spider_name)
    spider = getattr(module, spider_name)
    s = spider()
    s.run()
    print(s.result, len(s.result))


if __name__ == '__main__':
    time = timeit.timeit("engine('jianshu')", setup="from __main__ import engine", number=1)
    print(time)
