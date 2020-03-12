
from multiprocessing.pool import ThreadPool


def fetch_url(url):
    print('Hello')

download_list = [1,2,3,4]
results = ThreadPool(20).imap_unordered(fetch_url, download_list)