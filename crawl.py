import asyncio
import aiohttp


class Spider(object):
    def __init__(self, num=3, url_list=None):
        self.queue = asyncio.Queue()
        self.result = []
        self.sema = asyncio.Semaphore(num)
        self.url_list = url_list

    async def fetch_async(self, method):
        while True:
            url = await self.queue.get()
            with (await self.sema):
                async with aiohttp.request(method=method, url='http://httpbin.org/get?a={}'.format(url)) as r:
                    print("get {}...".format(url))
                    data = await r.json()

            self.queue.task_done()
            await self.analysis(data)

    async def analysis(self, data):
        res = {
            "arg":data["args"]["a"],
            "origin":data["origin"],
            "url":data["url"]
        }
        self.result.append(res)

    async def start(self, item):
        fetch = asyncio.ensure_future(self.fetch_async('GET'))
        await self.queue.put(item)
        await self.queue.join()
        fetch.cancel()

    def __run__(self):
        loop = asyncio.get_event_loop()
        f = asyncio.wait([self.start(num) for num in self.url_list])
        loop.run_until_complete(f)
        loop.close()
        print(self.result)

if __name__ == '__main__':
    s = Spider(url_list=[1, 5, 6, 73, 4])
    s.__run__()
