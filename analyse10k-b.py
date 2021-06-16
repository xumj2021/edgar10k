import time
from lxml import etree
import csv
import re
from tqdm import tqdm
import requests
import json
import pandas as pd
import csv
import os
import re
from tqdm import tqdm
import unicodedata

fileadd = "/Users/mengjiexu/Dropbox/edgar10k/10khtm/"
os.chdir(fileadd)
file_list = os.listdir(fileadd)

def locatese(file):
    with open("/Users/mengjiexu/Dropbox/edgar10k/locatese.csv",'a') as f:
        g = csv.writer(f)

        data = open(file,'r').read()
        page = etree.HTML(data)
        mainlist = page.xpath("//*")
        index = 0
        indexlist = []
        start = 0
        for unit in mainlist:
            index += 1
            if unit.xpath("name()") == "b":
                indexlist.append(index)
                if unit.text!=None:
                    if re.findall("subsequent event", unit.text.lower()):
                        start = index

        startpos = indexlist.index(start)
        end = indexlist[startpos+1]
        target = ""
        itemnum = 0
        for pos in range(start-1,end):
            if mainlist[pos].text:
                target = target + unicodedata.normalize('NFD',mainlist[pos].text).encode('ascii', 'ignore').decode('utf8') +"\n"
                itemnum += 1

        g.writerow([file, itemnum, target])

for file in tqdm(file_list):
    try:
        locatese(file)
    except:
        pass
