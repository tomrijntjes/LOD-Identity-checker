from retriever import Retriever
import time

#urls = ["http://index.lodlaundromat.org/r2d/http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23sameAs?page="+str(_) for _ in range(20)]
urls = ["https://www.google.nl/?gfe_rd=cr&ei=4GRnVcXfIsb--Qby54GIBA#q=1&safe=off&start="+str(_) for _ in range (0,500,10)]


for i in range(1,50):
  t=time.clock()
  Retriever(urls,'n',i)
  print("Throttle {0} fetches 20 urls in {1}".format(i,time.clock()-t))
