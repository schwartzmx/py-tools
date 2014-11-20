#!/usr/bin/env python

__author__ = 'Phil'

# Crawl the specified webpage.

import sys
import requests
from bs4 import BeautifulSoup
import argparse


bsoup = None
crawled_links = 1
max_crawl = None


def main():
    global max_crawl
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Specify a URL (Example: www.mysite.com)", action="store", type=str)
    parser.add_argument("maxLinksToCrawl", help="Specify the max amount of links to crawl. (100)", action="store",
                        type=int)
    args = parser.parse_args()

    if args.url and args.maxLinksToCrawl:
        max_crawl = args.maxLinksToCrawl
        url = args.url
        if not "http" in url:
            url = "http://" + url
        l = []
        try:
            bs_url(l, url)
        except:
            sys.exit(1)

    else:
        print  parser.usage


def bs_url(l, url):
    global bsoup

    try:
        r = requests.get(url)
        data = r.text
        bsoup = BeautifulSoup(data)
        spider(l, url)
    except:
        if crawled_links == max_crawl:
            sys.exit(0)
        print "> Broken link encountered. Skipping..."
        l.remove(url)


def spider(l, url):
    global bsoup
    global crawled_links, max_crawl
    http = 'http'
    for link in bsoup.find_all('a', href=True):
        linktext = link['href']
        if http in linktext:
            l.append(linktext)
            # print linktext
        else:
            linktext = url + linktext
            l.append(linktext)
            # print linktext

    for link in l:
        l.remove(link)
        print "Crawled Links:", crawled_links, "<> Current Link: " + link

        if crawled_links == max_crawl:
            print "Max crawls reached.  \nExited."
            sys.exit(0)

        crawled_links += 1
        bs_url(l, link)


if __name__ == "__main__":
    main()

