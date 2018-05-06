from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from reppy.robots import Robots
from reppy.cache import RobotsCache
import re
import requests
import queue
import time
import os
import signal

r = "http://www.codeforces.com"
i = 0

def robots(pathTotal, rp):
    return rp.allowed(pathTotal,"*")

def get_all_links(domain, pathTotal, maxSize, rp):
    #response = requests.get(domain+path, headers={'User-Agent': 'Mozilla/5.0'})
    driver = webdriver.PhantomJS( service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.get(pathTotal)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.service.process.send_signal(signal.SIGTERM)
    links = []
    for link in soup.findAll('a', href=True):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if(((re.match(regex, domain+link.get('href')) is not None or re.match(regex, domain+'/'+link.get('href')) is not None) and (re.match(regex, link.get('href')) is None) and (link.get('href')!='javascript:void();')) or (domain in link.get('href'))):
            if(len(link.get('href'))>0):
                if(domain in link.get('href')):
                    if(robots(link.get('href'), rp)):
                        #print(link.get('href'))
                        try:
                            r = requests.get(link.get('href'), verify=False)
                            if "text/html" in r.headers["content-type"]:    
                                links.append(link.get('href'))
                        except:
                            pass
                elif((link.get('href')[0]>='a'and link.get('href')[0]<='z') or (link.get('href')[0]>='1'and link.get('href')[0]<='9')):
                    if(robots(domain+'/'+link.get('href'), rp)):
                        #print(domain+'/'+link.get('href'))
                        try:
                            r = requests.get(domain+'/'+link.get('href'), verify=False)
                            if "text/html" in r.headers["content-type"]:    
                                links.append(domain+'/'+link.get('href'))
                        except:
                            pass
                else:
                    if(robots(domain+link.get('href'), rp)):
                        #print(domain+link.get('href'))
                        try:
                            r = requests.get(domain+link.get('href'), verify=False)
                            if "text/html" in r.headers["content-type"]:  
                                links.append(domain+link.get('href'))
                        except:
                            pass
        
    return links


def crawler(domain, pathseed, maxSize = 1000):
    q = queue.Queue()
    visited = []
    links = []
    q.put(domain+pathseed)
    visited.append(domain+pathseed)
    rp = Robots.fetch(domain+'/robots.txt',verify=False)
    while(not q.empty() and q.qsize()<maxSize):
        a = q.get()
        print("! " + str(len(links)))
        if(len(links) < maxSize):
            links.append(a)
            ls = get_all_links(domain, a, maxSize, rp)
            for l in ls:
                if(l not in visited):
                    visited.append(l)
                    q.put(l)
        else:
            while(not q.empty()):
                q.get()
    while(len(links)<maxSize and not q.empty()):
        links.append(q.get())
    os.makedirs('Docs/HTMLPages/BFS/'+folder(domain)+'/', exist_ok=True)
    print(len(links))
    v = 0
    for l in links:
        v += 1
        print(str(v)+ " "+l)
        driver = webdriver.PhantomJS( service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        driver.get(l)
        #print(driver.page_source)
        with open('Docs/HTMLPages/BFS/'+folder(domain)+'/'+str(v) +'-'+l.replace('/','*')+'.html', 'wb') as f:
            f.write(bytes(driver.page_source,'UTF-8'))
        driver.service.process.send_signal(signal.SIGTERM) 
    return 0


def folder(domain):
    if(domain=="http://www.codeforces.com"):
        return 'Codeforces'
    if(domain=='http://www.spoj.com'):
        return 'Spoj'
    if(domain=='https://dmoj.ca'):
        return 'Dmoj'
    if(domain=='https://wcipeg.com'):
        return 'Wcipeg'
    if(domain=='http://acm.timus.ru'):
        return 'Timus'
    if(domain=='https://www.urionlinejudge.com.br'):
        return 'Uri'
    if(domain=='https://leetcode.com'):
        return 'Leetcode'
    if(domain=='https://www.codechef.com'):
        return 'Codechef'
    if(domain=='https://a2oj.com'):
        return 'A2oj'

#Falta leetcode
crawler('https://wcipeg.com','')
crawler('http://www.codeforces.com','')
crawler('https://a2oj.com','')
#crawler('https://www.codechef.com','')
crawler('http://www.spoj.com','')
crawler('https://dmoj.ca','')
crawler('http://acm.timus.ru','')
#crawler('https://www.urionlinejudge.com.br','')
crawler('https://leetcode.com','')

rp = Robots.fetch('http://www.codeforces.com'+'/robots.txt',verify=False)
print(rp.allowed('http://www.codeforces.com','*'))
