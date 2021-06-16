import time
import json
import csv
import math
import requests
from tqdm import tqdm

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
           }

def postpage(year, page):
    come = (page-1)*100
    post = "{\"q\":\"\\\"subsequent event\\\"\",\"dateRange\":\"custom\",\"category\":\"custom\",\"startdt\":\"%s-01-01\",\"enddt\":\"%s-12-31\",\"forms\":[\"10-K\",\"10-Q\"],\"page\":\"%s\",\"from\":%s}"%(year,year,page,come)
    return(post)

def getinfo(year, page):    
    with open("edgarcookies.txt", "r")as f:
        cookies = f.read()
        cookies = json.loads(cookies)
        session = requests.session()

        url = "https://efts.sec.gov/LATEST/search-index"
        data = session.post(url,  headers=headers, cookies=cookies, data=postpage(year, page))
        time.sleep(1)

        info = json.loads(data.text)

        totalnum = info['hits']['total']['value']

        for case in info['hits']['hits']:
            with open('edgar10k.csv','a') as g:
                h = csv.writer(g)

                id = case['_id']
                try:
                    cik0 = case['_source']['ciks'][0]
                except:
                    cik0 = ""
                root_form = case['_source']['root_form']
                file_num = case['_source']['file_num']
                try:
                    display_names_0 = case['_source']['display_names'][0]
                except:
                    display_names_0 = ""
                file_date = case['_source']['file_date']
                adsh = case['_source']['adsh']

                out = [id,cik0,root_form, file_num, display_names_0,file_date,adsh]
                h.writerow(out)

        return(totalnum)

for year in range(2020, 2022):
    totalnum = getinfo(year,1)
    print(totalnum)
    pagenum = math.ceil(totalnum/100)+1
    print("%s %s"%(year,pagenum))
    for page in tqdm(range(2,pagenum)):
        getinfo(year,page)

