import os

if not os.path.isfile("endpoints.txt"):
    os.system("python3 fetcher.py")
else:
    os.system("python3 store_endpoints.py")
    os.system("python3 fetcher.py")
