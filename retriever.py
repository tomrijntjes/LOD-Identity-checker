import asyncio
import aiohttp
import pycurl
import time
from io import BytesIO


class Retriever:
    def __init__(self,urls,endpoints,throttle=10):
        self.total_urls = str(len(urls))
        if len(endpoints)==1:
            endpoints = [endpoints]*int(self.total_urls) #bit of a hack, needs work
        self.results = list()
        self.c = pycurl.Curl()
        self.sem = asyncio.Semaphore(throttle)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main(urls,endpoints))


    def __iter__(self):
        return self

    def __next__(self):
        if len(self.results) == 0:
            raise StopIteration
        return self.results.pop(0)

    def fetch_page1(self,url,idx):
        buffer = BytesIO()
        self.c.setopt(self.c.WRITEDATA, buffer)
        self.c.setopt(pycurl.URL, url)
        self.c.setopt(pycurl.HTTPHEADER, ["Accept: application/n-quads"])
        self.c.perform()
        body = buffer.getvalue()
        for statement in body.decode('utf-8').split('\n'):
            self.results.append(statement)
        buffer.close()

    def fetch_page(self,url, endpoint, idx):
        try:
            with (yield from self.sem):
                response = yield from aiohttp.request('GET', url,headers={"Accept": "application/n-quads"})
        except aiohttp.errors.ClientResponseError:
            print("[-]aiohttp.errors.ClientResponseError, pausing and continuing...")
            time.sleep(1)
            response = yield from aiohttp.request('GET', url)
        if response.status == 200:
            try:
                raw = yield from response.text()
                self.results.append([endpoint,url,raw])
            except UnicodeDecodeError: #needs works
                self.results.append([endpoint,url,'here be unicode'])
            print("[+] #{0}:{1}/{2}".format(str(idx+1),str(len(self.results)),self.total_urls))
        else:
            print("[-] Data fetch failed for: %d" % idx)
            print(response.content, response.status)
        response.close()

    def main(self,urls,endpoints):
        coros = []
        for idx, url in enumerate(urls):
            coros.append(asyncio.Task(self.fetch_page(url, endpoints[idx], idx)))

        yield from asyncio.gather(*coros)
