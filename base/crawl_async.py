
import asyncio
import aiohttp
from base.filter import BaseFilter
from settings import Queue_num, Semaphore_num, sleep_time
from time import sleep


class Spider(object):
    url_list = []
    method = 'get'
    http_type = ""
    loop = None
    session = None
    cookies = {}
    headers = {}
    queue = asyncio.Queue(Queue_num)
    sema = asyncio.Semaphore(Semaphore_num)

    def __init__(self):
        self.seen = BaseFilter()
        self.result = []

    async def request(self, request_dict):
        url = request_dict['url']
        headers = request_dict.get('headers', self.headers)
        cookies = request_dict.get('cookies', self.cookies)
        http_type = request_dict.get('http_type', self.http_type)
        try:
            with self.session or aiohttp.ClientSession(cookies=cookies, conn_timeout=1, read_timeout=1) as session:
                async with session.request(method=self.method, url=url,
                                           headers=headers, timeout=2) as r:
                    print("get -> {}".format(url), "<code %s>" % str(r.status))
                    if r.status == 200:
                        if http_type == "json":
                            data = await r.json()
                        elif http_type == "read":
                            data = await r.read()
                        else:
                            data = await r.text()
                    else:
                        data = await None
                await asyncio.sleep(sleep_time)
                return data, r
        except TimeoutError as te:
            print('timeoutError:' + str(te))
            return None, None

    async def fetch_async(self):
        while True:
            request_dict = await self.queue.get()
            if isinstance(request_dict, dict) and request_dict['url']:
                url = request_dict['url']
                if self.seen.add(url):
                    with (await self.sema):
                        data, r = await self.request(request_dict)
                    await self.analysis_async(data, r)
                    self.queue.task_done()
                else:
                    self.queue.task_done()
            else:
                await asyncio.sleep(1)
                print('pass None url')
                self.queue.task_done()

    async def analysis_async(self, data, resp):
        res = self.parser(data, resp)
        if res:
            self.result.append(res)

    async def start_async(self, item):
        fetch = asyncio.ensure_future(self.fetch_async())
        await self.queue.put(item)
        await self.queue.join()
        fetch.cancel()


    def run(self):
        self.url_list.append({'url':None})
        self.loop = asyncio.get_event_loop()
        f = asyncio.wait([self.start_async(url) for url in self.url_list])
        try:
            self.loop.run_until_complete(f)
        except Exception:
            print("exception consumed")
            for task in asyncio.Task.all_tasks():
                task.cancel()
            self.loop.run_forever()
        finally:
            self.loop.close()

    async def stop(self):
        while True:
            if self.queue.empty():
                print('check')
                sleep(1)
                if self.queue.empty():
                    print('stop')
                    self.loop.close()

    def parser(self, data, resp):
        # 解析数据
        return data

    def put_url(self, url_dict):
        # 添加协程进入事件循环
        # asyncio.ensure_future(self.put_async(url))

        self.loop.create_task(self.put_async(url_dict))

    async def check(self, url):
        if not self.seen.add(url):
            return False

    async def put_async(self, request_dict):
        # 将需要爬取的url放入队列
        await self.queue.put(request_dict)
        print("put -> {}".format(request_dict['url']))


if __name__ == '__main__':
    s = Spider()
    s.url_list = [1, 6, 7, 34, 53]
    s.run()