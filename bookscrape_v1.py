
from multiprocessing import Pool, Lock, Manager
import multiprocessing
import requests
import time
from datetime import datetime
import random
import settings
from bs4 import BeautifulSoup
import re
import os
import urllib2
import eventlet
from eventlet.green import urllib2
import urllib2
from requests.exceptions import *


def saved_proxies():
    f = open('proxylist.csv','r')
    text = f.readlines()
    freshproxlist = []
    for line in text:
        prox ={
            'http':'http://sk004:cpUGUJ4L@{}:60099/'.format(line.strip()),
            'https':'https://sk004:cpUGUJ4L@{}:60099/'.format(line.strip())
            }
        freshproxlist.append( prox )
    return freshproxlist

proxylist = saved_proxies()

def log(msg):
    # global logging function
    if settings.log_stdout:
        try:
            print "{}: {}".format(datetime.now(), msg)
        except UnicodeEncodeError:
            pass  # squash logging errors in case of non-ascii text
        

#*#Enters url in question then successfully obtain/return soup object.
##def make_request(url):
##    global proxylist
##    proxy = random.choice(proxylist)
##    try:
##        r = requests.get(url, headers=settings.headers, proxies=proxy)
##    except RequestException as e:
##        log("WARNING: Request for {} failed, trying again.".format(url))
##        return make_request(url)  # try request again, recursively
##    
##    html = r.content
##    
##    if r.status_code != 200:
##        log("WARNING: Got a {} status code for URL: {}".format(r.status_code, url))
##
##        return make_request(url)
##
##    if len(html) < 100000:
##        print proxy
##        log("WARNING: {} status_code URL: {} len(html): {} proxy: ".format(r.status_code, url,len(html),proxy) )
##
##        return make_request(url)
##    
##
##    soup = BeautifulSoup(html,'html.parser')
##    log("Success! {} {} len(html) {}".format(url, proxy,len(html)))
##    return soup

def make_request(url):
    global proxylist
    while True:
        try:
            proxy = random.choice(proxylist)
            r = requests.get(url, allow_redirects = False, headers = settings.headers, proxies = proxy, timeout = 10)
            html = r.content
            if len(html) < 100000:
                print ("WARNING: {} status_code URL: {} len(html): {} proxy: ".format(r.status_code, url,len(html),proxy) )
            else: break            
        except (ConnectTimeout,ReadTimeout,ChunkedEncodingError,ProxyError,ConnectionError,ContentDecodingError,TooManyRedirects):
            print ("WARNING: URL: {} proxy: ".format( url, proxy) )
    print ("Success! {} {} len(html) {}".format(url, proxy,len(html)))
    soup = BeautifulSoup(html,'html.parser')
    return unicode(soup.title).encode('ascii','ignore')


    
def get_tiv(soup):
    tradeinvalue = soup.find('div',attrs={'id':'tradeInButton'})
    if not tradeinvalue:
        log("TIV does not exist")
        return None
    tradeinvaluetext = unicode(tradeinvalue).encode('ascii','ignore')
    tradeinvalue =  re.findall('\$([0-9.]+)',tradeinvaluetext)[0].replace(',','').replace('$','')
    log("TIV Found: {}".format(tradeinvalue))
    return tradeinvalue


def get_azprice(soup):
    ## Doesn't have landing format
    azpricebox = soup.find('li',attrs={'class':'swatchElement selected'})
    if not azpricebox:
        azprice = soup.find('div',attrs={'id':'mediaTab_content_landing'})
        if not azprice:
            log("No price information exists")
            return None
        azprice = soup.find('div',attrs={'class':'a-box a-accordion-active accordion-row'})
        if not azprice:
            azprice = soup.find('span',attrs={'class':'a-size-medium a-color-price header-price'})
            if not azprice:
                log("Landing page recognized, but azpriceused not found")
                return None
        else:
            azprice = azprice.find('span',attrs={'class':'a-size-medium a-color-price header-price'})
            if not azprice:
                log("Landing Page recognized, buybox recognized, but No price information exists")
                return None
    else:
        azprice = azpricebox.find('span',attrs={'class':'a-color-price'})
        if not azprice:
            log("azpricebox exists but azprice does not exist")
            return None

    azpricetext = azprice.string
    azprice =  re.findall('\$([0-9.]+)',azpricetext)[0].replace(',','').replace('$','')
    log("AZprice Found: {}".format(azprice))
    return azprice
        

if __name__ == '__main__':
    
    
    log("Reading isbns.txt")
    text_file = open('isbns.txt','r')
    isbns = text_file.read()
    isbns = isbns.strip()
    isbns = isbns.split()
    text_file.close()
    log("{} isbns ready for scraping".format(len(isbns)))

    urls = []
    for isbn in isbns:
        url = "https://www.amazon.com/gp/product/" + isbn
        urls.append(url)
        
    urls = urls[0:100]
    
    start = time.time()
    p = Pool(4)
    result = p.map(make_request,urls)
    p.close()
    p.join() 
    print 'Runtime: %ss' % (time.time()-start)
