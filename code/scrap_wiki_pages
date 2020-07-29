import os
import json
import requests
import pandas as pd
import multiprocessing
import urllib.request
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                     "Accept-Encoding":"gzip, deflate",
                     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1",
                     "Connection":"close", "Upgrade-Insecure-Requests":"1"}

def scarp_wikipages(urls_list):
    print(urls_list)
    try:
        url = urls_list['WikiURL']
        res = requests.get(url, headers = headers)
        wiki = BeautifulSoup(res.text, "html.parser")
        para = ""
        for i in wiki.select('p'):
            para = para + i.getText()

        if para == 'Other reasons this message may be displayed:':
            urls_list['Text'] = "Data not available"
        else
            urls_list['Text'] = para
    finally:
        return urls_list


if __name__ == '__main__':

    url = "https://en.wikipedia.org/wiki/List_of_OMIM_disorder_codes"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    urls_list = pd.DataFrame(columns=["OMIM ID", "WikiURL"])
    all_list = soup.find_all('li')
    
    rows = []

    for link in all_list:
        href = ""
        for results in link.findAll('a'):  
            if href == "":
                href = str("https://en.wikipedia.org" + results.get('href'))

            if results.contents:
                ans = str(results.contents[0])
                if ans.isnumeric():
                    new_row = {"OMIM ID": ans, "WikiURL": href}
                    rows.append(new_row)
                    #urls_list = urls_list.append(new_row, ignore_index=True);
                    break


    workers = max(os.cpu_count()-1,1)
    manager = multiprocessing.Manager()
    listManager = manager.list()
    pool = multiprocessing.Pool(workers)

    try:
        complete_result = pool.map(scarp_wikipages, rows)
        pool.close()
        pool.join()
    finally:
        for row in complete_result:
            urls_list = urls_list.append(row, ignore_index=True)
            
        urls_list.to_csv("wikipage.csv")
