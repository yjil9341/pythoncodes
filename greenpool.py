import eventlet
from eventlet.green import urllib2
import time


urls = ["http://www.google.com/intl/en_ALL/images/logo.gif",
       "https://www.python.org/static/img/python-logo.png",
       "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif"]        
urls = urls*333000

def fetch(url):
    return urllib2.urlopen(url).read()
print "Reading urls: ", len(urls)

print len(urls)

beg = time.time()
pool = eventlet.GreenPool()
for body in pool.imap(fetch, urls):
    pass
##    print("got body", len(body))
print "Run time was: %ss" %(str(time.time()-beg))
