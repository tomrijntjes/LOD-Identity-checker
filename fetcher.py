import json
import urllib.request
import codecs
import pycurl
from io import BytesIO

def stream_statements(endpoints,pages=1):
    c = pycurl.Curl()
    counter = 1
    for endpoint in endpoints:
        print("Visiting endpoint #{0}: {1}".format(str(counter),endpoint))
        buffer = BytesIO()
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(pycurl.URL, "http://ldf.lodlaundromat.org/"+endpoint+"?predicate=http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs&page=1")
        c.setopt(pycurl.HTTPHEADER, ["Accept: application/n-quads"])
        c.perform()
        body = buffer.getvalue()
        for statement in body.decode('utf-8').split('\n'):
            yield statement
        buffer.close()
        counter+=1


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

def sameAs_count(statements):
    running_count = 0
    for statement in statements:
        if "totalItems" in statement:
            sameAs = statement.split('"')[1]
            if sameAs:
                running_count += int(sameAs)
                print(running_count)
                yield int(sameAs)

def tests():
    assert len(list(stream_endpoints("http://index.lodlaundromat.org/r2d/http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs?page=")))<10000
    print("[+] stream_endpoints OK")
    statements = list(stream_statements(["0032d1f3c356798f23cb89874eaabb98","01abf0f5914a8b6c9e48980aacb9ddad"]))
    print("[+] Example statements {0}".format(statements[3:5]))
    try:
        assert len(statements) == len(set(statements))
    except AssertionError:
        print("[-] {0} duplicates found in a total of {1} statements".format(len(statements) - len(set(statements)),len(statements)))
        raise
    print("[+] no duplicates found, stream_statements OK")


if __name__ == '__main__':
    #tests()
    url = "http://index.lodlaundromat.org/r2d/http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs?page="
    endpoints = stream_endpoints(url)
    statements = stream_statements(endpoints)
    tally = list(sameAs_count(statements))
    print("Visited {0} endpoints, containing a total of {1} sameAs statements".format(str(len(tally)),str(sum(tally))))
