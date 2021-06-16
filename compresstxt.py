import os
import pandas as pd
import json
import csv
from tqdm import tqdm
import requests
import re
from bs4 import BeautifulSoup
import unicodedata



path = "/Users/mengjiexu/Dropbox/edgar10k/10ktxt"
newpath = "/Users/mengjiexu/Dropbox/edgar10k/10ktxtcompressed"
file_list = os.listdir(path)


def compress(file_path):
	content = open('%s/%s'%(path,file_path)).read()
	newcontent = re.sub("\n+","\n",content)
	with open('%s/%s'%(newpath,file_path),'w') as f:
		f.write(newcontent)

for file in tqdm(file_list):
	try:
		compress(file)
	except:
		print("\n"+file)
	
		