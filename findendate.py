import csv
import os
from tqdm import tqdm
import re 

path = "/Users/mengjiexu/Dropbox/edgar10k/10ktxtcompressed"
file_list = os.listdir(path)

def getendate(file):
	with open("endate.csv",'a') as f:
		g = csv.writer(f)

		with open('%s/%s'%(path,file),'r') as f:
			content = f.readlines()
		
		comment = re.compile(r'[A-Z][a-z]+ [\d]+, [\d]+\s', re.DOTALL)
		date = [x for x in range(len(content)) if comment.search(content[x])]

		if date:
			dateline = [content[x]+'\n' for x in range(date[0]-2, date[0]+1)]
			fulldate = " ".join(dateline)
			puredate = content[date[0]]
			g.writerow([file,fulldate,puredate])
		

for file in tqdm(file_list):
	getendate(file)