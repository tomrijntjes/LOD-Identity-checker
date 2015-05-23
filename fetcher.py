import json
import urllib.request
import codecs
from retriever import Retriever
import aiohttp
import sys


def stream_pages(file):
    with open(file) as endpoints:
        for line in endpoints:
            endpoint,pagecount = line.split('\t')
            url = "http://ldf.lodlaundromat.org/"+endpoint+"?predicate=http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs&page="
            pages = [url+str(page) for page in range(1,1+int(pagecount))]
            for endpoint,url,page in Retriever(pages,[endpoint]):
                yield endpoint,page

def stream_quads(pages):
    for page in pages:
        endpoint = " <http://lodlaundromat.org/resource/"+page[0][0]+">."
        for statement in page[1].split('\n'):
            triple = statement.split(' ')
            if len(triple) == 3 and triple[1]=="<http://www.w3.org/2002/07/owl#sameAs>":
                yield statement[:-1]+endpoint+"\n"

if __name__ == '__main__':
    pages = stream_pages("endpoints.txt")
    with open("identity.nq","w") as f:
        for quad in stream_quads(pages):
            f.write(quad)
