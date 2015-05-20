import json
import urllib.request
import codecs
import pycurl
from io import BytesIO

endpoints = []


def get_endpoints():
    print("getting endpoints")
    pagesize, page = 1,1
    url = "http://index.lodlaundromat.org/r2d/http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs?page="
    reader = codecs.getreader("utf-8")
    while pagesize>0:
        raw = urllib.request.urlopen(url+str(page))
        data = json.load(reader(raw))
        
        pagesize = int(data['pageSize'])
        for endpoint in data['results']:
            endpoints.append(endpoint)
        page+=1
    
    return endpoints


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
            #print("using endpoint " + str(endpoint) + " :")
            #print(str(body) + "\n\n")
            for statement in body.decode('utf-8').split():
                
                yield statement

def stream_endpoints(url):
    pagesize,page = 1,1
    reader = codecs.getreader("utf-8")
    while pagesize>0:
        print(page)
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


def extractNumber(statement):
    number = statement.split('"')[1]
    return number

def getNumberOfSameAs(endpoint):
    c = pycurl.Curl()
    buffer = BytesIO()
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(pycurl.URL, "http://ldf.lodlaundromat.org/"+endpoint+"?predicate=http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs&page=1")
    c.setopt(pycurl.HTTPHEADER, ["Accept: application/n-quads"])
    c.perform()
    body = buffer.getvalue()
    for statement in body.decode('utf-8').split('\n'):
        if "totalItems" in statement:
            #print(endpoint)
            number = extractNumber(statement)
            return number
            '''
            intNumber = int(number)
            if isinstance(intNumber, int):
                return intNumber
            else:
                return 0
            '''
            #print(endpoint + " has number of sameAs: "+ number + "\n\n\n")
            
    
    


if __name__ == '__main__':
    url = "http://index.lodlaundromat.org/r2d/http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs?page="
    endpoints = get_endpoints()
    
    totalSameAs = 0
    counter = 0
    
    for endpoint in endpoints:
        #totalSameAs +=getNumberOfSameAs(endpoint)
        f = open("C:/users/sietse/desktop/sameAsResults_v1.txt",'a')
        writeString = endpoint + ": " + str(getNumberOfSameAs(endpoint))
        print(str(counter) + ": " + str(writeString))
        f.write(writeString)
        counter+=1
        f.close()
        #print(str(counter) + ": " + str(totalSameAs))
        #print(counter)
    
    
    '''
    endpoints = stream_endpoints(url)
    
    
    #endpoints = ["0032d1f3c356798f23cb89874eaabb98"]
    pages = 1 #still needs a reliable way of finding the number of pages per endpoint
    statements = stream_statements(endpoints,pages)
    triples = splat_statements(statements)
    counter = 0
    for triple in triples:
        #print(triple)
        counter+=1
    print(counter)
    '''
