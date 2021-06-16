from lxml import etree
import csv
import os
import re
from tqdm import tqdm
import unicodedata

fileadd = "/Users/mengjiexu/Dropbox/edgar10k/10khtm/"
os.chdir(fileadd)
file_list = os.listdir(fileadd)

def locatese(file):
    with open("/Users/mengjiexu/Dropbox/edgar10k/locatese-bold.csv",'a') as f:
        g = csv.writer(f)

        page = etree.parse(file)

        mainlist = page.xpath("//*")

        index = 0
        start = 0
        indexlist = []
        for unit in mainlist:
            index += 1
            for tags in unit.findall('.//'): #not sure whether element.values will also extract all descendant... remove this if it does
                values = values + ',' + ", ".join(tags.values())
            if re.findall("bold", values):
                indexlist.append(index)
                if unit.text:
                    content = " ".join(unit.itertext()).lower()
                    if re.findall(r"subsequent event|subsequent events", content,flags=re.IGNORECASE): #different spellings and case unsensitive
                        start = index

        startpos = indexlist.index(start)
        end = indexlist[startpos+1]
        target = ""
        itemnum = 0
        for pos in range(start-1,end+1):
            if mainlist[pos].text:
                target = target + unicodedata.normalize('NFD',mainlist[pos].text).encode('ascii', 'ignore').decode('utf8') +"\n"
                itemnum += 1

        g.writerow([file, itemnum, target])

for file in tqdm(file_list):
    try:
        locatese(file)
    except:
        pass