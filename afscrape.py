#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import sys
import argparse
import json

def main():

    parser = argparse.ArgumentParser(description='Andhra Friends scraping')
    parser.add_argument('-pagelimit', default = 2350, type=int, help='How many pages you want to scrape')
    parser.add_argument('--dump', action='store_true', help='dump JSON results')
    parser.add_argument('--savejson', action='store_true', help='save results to JSON file')
    # parser.add_argument('--savecsv', action='store_true', type=float, help='dump results')
    with open('outfile4.json', "wb") as w:
        def scrapethread(link):
            acc = []
            r = requests.get(link + "?page=1")
            data = r.text
            soup = BeautifulSoup(data, "html5lib")
            comments = soup.find_all('article')
            for comment in comments:
                unwanted = comment.find('blockquote')
                if(unwanted):
                    unwanted.extract()
                wrap = comment.find('div', class_='ipsColumn').find_next('div')
                commentdata = wrap.find('div', class_='ipsType_normal').get_text()
                commentdata = commentdata.replace('\n', ' ').replace('\t','').replace(u'\u00a0', ' ')
                if("".join(commentdata.split())==""):
                    continue
                objdata = wrap['data-quotedata']
                pyobjdata = json.loads(objdata)
                pyobjdata["content"] = commentdata
                acc.append(json.dumps(pyobjdata))
                w.write(json.dumps(pyobjdata) + "\n")
                # print(repr(commentdata))
            return acc

        def scrape(pagelimit):
            count = 0
            acc = []
            for i in range(1, pagelimit+1):
                r = requests.get("http://www.andhrafriends.com/forum/48-discussions/?page=" + str(i))
                data = r.text
                soup = BeautifulSoup(data, "html5lib")
                items = soup.find("ol")
                if(items == None):
                    print("page " + str(i) + "is NoneType")
                    continue
                for link in items.find_all('a'):
                    if(count>=100000):
                        return res
                    nexthref = link.get('href')
                    if("?page=" not in nexthref and "?do=getLastComment" not in nexthref and "/tags/" not in nexthref):
                        nextres = scrapethread(nexthref)
                        count+=len(nextres)
                        acc.extend(nextres)
                print("finished page " + str(i) + ", size " + str(len(acc)))
            return acc


        args = parser.parse_args()

        res = scrape(args.pagelimit)

        if(args.dump):
            print(res)
        if(args.savejson):
            print(str(len(res)) + " instances scraped.")

main()
