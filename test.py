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

# import requests
#
# url = "http://www.jianshu.com/p/deae0356a1df"
#
# item_header = {
#         "Host": "www.jianshu.com",
#         "Connection": "keep-alive",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
#         "Referer": "http://www.jianshu.com/search?q=python&page=1&type=note",
#         "Accept - Encoding": "gzip, deflate",
#         "Accept - Language": "zh-CN,zh;q=0.8",
#     }
#
#
# html = requests.get(url,headers=item_header)
#
# print(html.text,html.url,html.status_code)

def run(data):
    backup_type = data['backup_type']
    backup_subtype = data['backup_subtype']
    backup_size = data['backup_size']

    incr_dict = {'key': 'Incr', 'label': '增量'}
    full_dict = {'key': 'Full', 'label': '全备'}
    oneday_dict = {'key': '1D', 'label': '每天一次'}
    oneweek_dict = {'key': '1W', 'label': '每周一次'}
    res = []
    if backup_type == 'Oracle':
        full_dict['rate'] = oneweek_dict
        incr_dict['rate'] = oneday_dict
        res = [full_dict, incr_dict]
    elif backup_type == 'OraArc':
        incr_dict['rate'] = {'key': '2H', 'label': '每两小时一次'}
        res.append(incr_dict)
    elif backup_type == 'SQL':
        if backup_subtype in ['两节点MSCS集群', '单节点SQL Server'] and int(backup_size) > 300:
            full_dict['rate'] = oneweek_dict
            incr_dict['rate'] = oneday_dict
            res = [full_dict, incr_dict]
        elif backup_subtype == '三节点Always-On' or int(backup_size) <= 300:
            full_dict['rate'] = oneday_dict
            res.append(full_dict)
    elif backup_type == 'File':
        full_dict['rate'] = oneday_dict
        incr_dict['rate'] = oneday_dict
        res = [full_dict, incr_dict]

    return res


if __name__ == '__main__':
    data = {
        'backup_type': 'OraArc',
        'backup_subtype': '两节点MSCS集群',
        'backup_size': '3'
    }
    print(run(data))
