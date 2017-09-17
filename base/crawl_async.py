import asyncio
import aiohttp
from base.filter import BaseFilter
from settings import Queue_num, Semaphore_num, sleep_time


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

    async def request(self, url):
        with self.session or aiohttp.ClientSession(cookies=self.cookies,conn_timeout=2) as session:
            async with session.request(method=self.method, url=url,
                                       headers=self.headers) as r:
                print("get -> {}".format(url), "<code %s>" % str(r.status))
                if self.http_type == "json":
                    data = await r.json()
                elif self.http_type == "read":
                    data = await r.read()
                else:
                    data = await r.text()
            await asyncio.sleep(sleep_time)
            return data, r

    async def fetch_async(self):
        while True:
            url = await self.queue.get()
            if self.seen.add(url):
                with (await self.sema):
                    data, r = await self.request(url)
                await self.analysis_async(data, r)
                self.queue.task_done()
            else:
                self.queue.task_done()

    async def analysis_async(self, data, resp):
        res = self.parser(data, resp)
        self.result.append(res)

    async def start_async(self, item):
        fetch = asyncio.ensure_future(self.fetch_async())
        await self.queue.put(item)
        await self.queue.join()
        fetch.cancel()

    def run(self):
        self.loop = asyncio.get_event_loop()
        f = asyncio.wait([self.start_async(url) for url in self.url_list])
        self.loop.run_until_complete(f)
        self.loop.close()

    def parser(self, data, resp):
        # 解析数据
        return data

    def put_url(self, url):
        # 添加协程进入事件循环
        # asyncio.ensure_future(self.put_async(url))

        task = self.loop.create_task(self.put_async(url))
        print(task)

    async def check(self, url):
        if not self.seen.add(url):
            return False

    async def put_async(self, url):
        # 将需要爬取的url放入队列
        await self.queue.put(url)
        print("put -> {}".format(url))


if __name__ == '__main__':
    s = Spider()
    s.url_list = [1, 6, 7, 34, 53]
    s.run()
