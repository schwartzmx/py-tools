#!/usr/bin/env python

__author__ = 'Phil'

#Crawl the specified webpage.

import sys
import requests
from bs4 import BeautifulSoup

bsoup = None

def bs_url(l, url):
    global bsoup
    r = requests.get(url)
    data = r.text
    bsoup = BeautifulSoup(data)
    spider(l,url)

def spider(l,url):
    global bsoup
    http = 'http'
    for link in bsoup.find_all('a', href=True):
        linktext = link['href']
        if http in linktext:
            l.append(linktext)
            print linktext
        else:
            linktext = url+linktext
            l.append(linktext)
            print linktext


    for link in l:
        l.remove(link)
        bs_url(l,link)


url = sys.argv[1]
url = "http://"+url
l = []
bs_url(l,url)

sys.exit()