import json
import urllib.request
import codecs
from retriever import Retriever
import aiohttp
import sys


def stream_pages(endpoints):
    urls = ["http://ldf.lodlaundromat.org/"+endpoint+"?predicate=http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs&page=" for endpoint in endpoints]
    for page,url,endpoint in zip(Retriever(urls),urls,endpoints):
        for statement in page.split('\n'):
            if "totalItems" in statement:
                statements = int(statement.split('"')[1])
                break
        if statements%100 == 0:
            pagecount = statements/100
        else:
            pagecount = int(statements/100) + 1
        pages = [url+str(page) for page in range(1,1+pagecount)]
        for page in Retriever(pages):
            yield endpoint,page


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

def stream_quads(pages):
    for page in pages:
        endpoint = " <http://lodlaundromat.org/resource/"+page[0]+">."
        for statement in page[1].split('\n'):
            triple = statement.split(' ')
            if len(triple) == 3 and triple[1]=="<http://www.w3.org/2002/07/owl#sameAs>":
                yield statement[:-1]+endpoint+"\n"




if __name__ == '__main__':
    url = "http://index.lodlaundromat.org/r2d/http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs?page="
    endpoints = list(stream_endpoints(url))
    #endpoints = ["03f8be0fbfe4d7529bb93c14ee1c65e7","057c1d67ebb7d7aa039c53da9e913f66"]
    pages = stream_pages(endpoints)
    with open("identity.nq","w") as f:
        for quad in stream_quads(pages):
            f.write(quad)
