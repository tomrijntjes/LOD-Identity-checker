import json
import urllib.request
import codecs
from retriever import Retriever
import aiohttp
import sys

def stream_pages(endpoints):
    urls = ["http://ldf.lodlaundromat.org/"+endpoint+"?predicate=http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs&page=" for endpoint in endpoints]
    for endpoint,url,page in Retriever(urls,endpoints,verbose=True):
        statements = 0
        for statement in page.split('\n'):
            if "totalItems" in statement:
                statements = int(statement.split('"')[1])
                break
        if statements%100 == 0:
            pagecount = int(statements/100)
        else:
            pagecount = int(statements/100) + 1
        yield "{0}\t{1}\t{2}\n".format(endpoint,pagecount,statements)


def stream_endpoints(url):
    pagesize,page = 1,1
    reader = codecs.getreader("utf-8")
    while pagesize>0:
        raw = urllib.request.urlopen(url+str(page))
        data = json.load(reader(raw))
        pagesize = int(data['pageSize'])
        for endpoint in data['results']:
            yield endpoint
        page+=1


if __name__ == '__main__':
    url = "http://index.lodlaundromat.org/r2d/http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs?page="
    endpoints = list(stream_endpoints(url))
    #endpoints = ["03f8be0fbfe4d7529bb93c14ee1c65e7","057c1d67ebb7d7aa039c53da9e913f66"]
    pages = stream_pages(endpoints)
    with open("endpoints.txt","w") as f:
        for page in pages:
            f.write(page)
    print("Total pages: " + str(sum(int(endpoint.split()[1]) for endpoint in open("endpoints.txt"))))
    print("Total statements: " + str(sum(int(endpoint.split()[2]) for endpoint in open("endpoints.txt"))))
