import asyncio
import aiohttp
from settings import Queue_num, Semaphore_num


class Spider(object):
    url_list = []
    queue = asyncio.Queue(Queue_num)
    result = []
    sema = asyncio.Semaphore(Semaphore_num)

    @classmethod
    async def fetch_async(cls, method):
        while True:
            url = await cls.queue.get()
            with (await cls.sema):
                async with aiohttp.request(method=method, url='http://httpbin.org/get?a={}'.format(url)) as r:
                    print("get {}...".format(url))
                    data = await r.json()

            cls.queue.task_done()
            await cls.analysis(data)

    @classmethod
    async def analysis(cls, data):
        res = {
            "arg": data["args"]["a"],
            "origin": data["origin"],
            "url": data["url"]
        }
        cls.result.append(res)

    @classmethod
    async def start(cls, item):
        fetch = asyncio.ensure_future(cls.fetch_async('GET'))
        await cls.queue.put(item)
        await cls.queue.join()
        fetch.cancel()

    @classmethod
    def run(cls):
        loop = asyncio.get_event_loop()
        f = asyncio.wait([cls.start(num) for num in cls.url_list])
        loop.run_until_complete(f)
        loop.close()
        print(cls.result)


if __name__ == '__main__':
    Spider.run()
