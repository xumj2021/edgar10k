import os
import pandas as pd
import json
import csv
from tqdm import tqdm
import requests
import re


df = pd.read_csv("edgar10k.csv",header=None)

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
           }

with open("edgarcookies.txt", "r")as f:
	cookies = f.read()
	cookies = json.loads(cookies)
	session = requests.session()

for row in tqdm(df.iterrows()):
	print(row[1][0])
	filenum = row[1][0].split(":")[0].replace("-","")
	print(filenum)
	url = filenum+"/"+row[1][0].split(":")[1]
	cik = "%010d" % row[1][1]
	filedate = row[1][5].replace('/','-')
	filename = "%s_%s"%(filedate,row[1][0])
	href=  "https://www.sec.gov/Archives/edgar/data/%s/%s"%(cik,url)
	print(href+"\n")
	data = session.get(href,  headers=headers, cookies=cookies)
	with open("/Users/mengjiexu/Dropbox/edgar10k/%s"%filename,'wb') as g:
		g.write(data.content)
 