import json
import urllib.request
import codecs
import pycurl
from io import BytesIO

def stream_statements(endpoints,pages):
    c = pycurl.Curl()
    buffer = BytesIO()
    c.setopt(c.WRITEDATA, buffer)
    for endpoint in endpoints:
        for page in range(pages):
            c.setopt(pycurl.URL, "http://ldf.lodlaundromat.org/"+endpoint+"?predicate=http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs&page="+str(page))
            c.setopt(pycurl.HTTPHEADER, ["Accept: application/n-quads"])
            c.perform()
            body = buffer.getvalue()
            for statement in body.decode('utf-8').split():
                yield statement

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

def splat_statements(statements):
    sameAs = "<http://www.w3.org/2002/07/owl#sameAs>"
    third,second,first = ' ',' ',' '
    for statement in statements:
        third,second,first = statement,third,second
        if third[-1]=='.' and second == sameAs: #this feels kind of crude
            yield (first,second,third)





if __name__ == '__main__':
    url = "http://index.lodlaundromat.org/r2d/http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs?page="
    endpoints = stream_endpoints(url)
    #endpoints = ["0032d1f3c356798f23cb89874eaabb98"]
    pages = 1 #still needs a reliable way of finding the number of pages per endpoint
    statements = stream_statements(endpoints,pages)
    triples = splat_statements(statements)
    counter = 0
    for triple in triples:
        print(triple)
        counter+=1
    print(counter)
