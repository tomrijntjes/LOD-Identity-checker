from retriever import Retriever
import time
import urllib.request

from operator import itemgetter



urls = ["http://index.lodlaundromat.org/r2d/http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs?page="+str(_) for _ in range(10)]
#urls = ["https://www.google.nl/?gfe_rd=cr&ei=4GRnVcXfIsb--Qby54GIBA#q=1&safe=off&start="+str(_) for _ in range (0,500,10)]


results = list()


for i in range(1,20):
  t=time.clock()
  Retriever(urls,'n',i)
  result = time.clock()-t
  results.append(result)
  print("Throttle {0} fetches {1} urls with {2} per url".format(i,len(urls),(result)/len(urls)))

print(min(results))
best = min(enumerate(results), key=itemgetter(1))[0]+1
print(best)
print("Throttle {0} achieves the best result: {1} as fast".format(best,1/((results[0]-min(results))/results[0])))
