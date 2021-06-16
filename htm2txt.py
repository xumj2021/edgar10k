import os
import pandas as pd
import json
import csv
from tqdm import tqdm
import requests
import re
from bs4 import BeautifulSoup
import unicodedata



file_list = os.listdir("/Users/mengjiexu/Dropbox/edgar10k/10khtm/")

def convert_htm_to_string(file_path):
	html = open(file_path).read()
	soup = BeautifulSoup(html)
	content = soup.get_text("\n").replace('\n','\n\n').replace(u'\xa0', u' ')
	return(content)

for file in tqdm(file_list):
	filename = file.split("/")[-1].split(".")[0]
	with open("/Users/mengjiexu/Dropbox/edgar10k/10ktxt/%s.txt"%filename, 'w') as f:
		try:
			content = convert_htm_to_string("/Users/mengjiexu/Dropbox/edgar10k/10khtm/"+file)
			f.write(content)
		except:
			print(file)
		