import time
import json
import csv
import math
import requests
import datetime
from tqdm import tqdm
import pandas as pd

df = pd.read_csv("/Users/mengjiexu/Dropbox/edgar10k/edgar10k.csv")

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
           }

def daterange(date, i):
    a = [int(x) for x in date.split("/")]
    date1 = datetime.datetime(a[0],a[1],a[2])
    start = date1 - datetime.timedelta(days=i)
    start = start.strftime("%Y-%m-%d")
    end = date1.strftime("%Y-%m-%d")
    return(start,end)

def postpage(start, end, cik, page):
    come = (page-1)*100
    post = "{\"dateRange\":\"custom\",\"category\":\"custom\",\"ciks\":[\"%s\"],\"startdt\":\"%s\",\"enddt\":\"%s\",\"forms\":[\"8-K\"],\"page\":\"%s\",\"from\":%s}"%(cik,start,end,page,come)
    return(post)

def getinfo(start, end, cik, page, oriname):    
    with open("edgarcookies.txt", "r")as f:
        cookies = f.read()
        cookies = json.loads(cookies)
        session = requests.session()

        url = "https://efts.sec.gov/LATEST/search-index"
        data = session.post(url,  headers=headers, cookies=cookies, data=postpage(start, end, cik, page))
        time.sleep(1)

        info = json.loads(data.text)

        totalnum = info['hits']['total']['value']

        for case in info['hits']['hits']:
            with open('/Users/mengjiexu/Dropbox/edgar10k/edgar8k.csv','a') as g:
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

                out = [id,cik0,root_form, file_num, display_names_0,file_date, adsh, start, end, oriname]
                h.writerow(out)

        return(totalnum)

for row in tqdm(df.iterrows()):
    oriname = row[1][0]
    cik =  "%010d"%row[1][1]
    date = row[1][5]
    [start, end] = daterange(date, 90)
    try:
        totalnum = getinfo(start, end, cik, 1, oriname)
        pagenum = math.ceil(totalnum/100)+1
        for page in tqdm(range(2,pagenum)):
            getinfo(start, end, cik, page, oriname)
    except:
        print("\n"+oriname)

