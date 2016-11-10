import eventlet
from eventlet.green import urllib2
import time
from multiprocessing import Pool, Lock, Manager
import multiprocessing
import requests



def fetch(url):
    return urllib2.urlopen(url).read()



def green_pool(urls):
    beg = time.time()
    pool = eventlet.GreenPool()
    for body in pool.imap(fetch, urls):
        pass
    print "GreenPool Run time was: %ss" %(str(time.time()-beg))
    return None

def serialrun(urls):
    beg = time.time()
    for url in urls:
        response = requests.get(url)
        body = response.content
    print "Serial Run time was: %ss" %(str(time.time()-beg))
    return None

def multiprocessingrun(url):
    response = requests.get(url)
    body = response.content
    return None

if __name__ == '__main__':
    inp = raw_input("Enter the multiplying number: ")
    urls = ["http://www.google.com/intl/en_ALL/images/logo.gif",
       "https://www.python.org/static/img/python-logo.png",
       "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif"]        
    urls = urls*int(inp)
    print "Total Websites to be read: " , len(urls)


    serialrun(urls)
    
    beg = time.time()
    p = Pool(4)
    result = p.map(multiprocessingrun,urls)
    print "multiprocessing Run time was: %ss" %(str(time.time()-beg))
    
    green_pool(urls)
    
    
    
    

