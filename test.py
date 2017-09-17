# from threading import Thread
# import asyncio
# import time
# now = lambda :time.time()
#
# def start_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()
#
# async def do_some_work(x):
#     print('Waiting {}'.format(x))
#     await asyncio.sleep(x)
#     print('Done after {}s'.format(x))
#
# def more_work(x):
#     print('More work {}'.format(x))
#     time.sleep(x)
#     print('Finished more work {}'.format(x))
#
# start = now()
# new_loop = asyncio.new_event_loop()
# t = Thread(target=start_loop, args=(new_loop,))
# t.start()
# print('TIME: {}'.format(time.time() - start))
#
# asyncio.run_coroutine_threadsafe(do_some_work(6), new_loop)
# asyncio.run_coroutine_threadsafe(do_some_work(2), new_loop)

# from base.loader import ItemLoader
# from item import TestItem
#
# i = ItemLoader(TestItem, 'html')
# i.add_soup('name', 'name1')
# i.add_soup('num', '12')
# i.add_soup('url', 'wewda')
#
# b = TestItem()
# b.set('name', 'name12')
# b.set('num', '53')
# b.set('url', 'wdwvwe')
#
# print(i.item.get_all())

import re

url = "http://www.jianshu.com/search?q=python&page=1&type=note"

if re.match("^http://www\.jianshu\.com/search\?q.*",url):
    print(1)
else:
    print(123)