import csv
import os
from tqdm import tqdm

path = "/Users/mengjiexu/Dropbox/edgar10k/10ktxtcompressed"
file_list = os.listdir(path)

def getse(file):
	with open('selist.csv','a') as g:
		h = csv.writer(g)
		with open('%s/%s'%(path,file),'r') as f:
			content = f.readlines()

		index = [x for x in range(len(content)) if 'Subsequent Event' in content[x]]

		for line in index:
			cut = [content[x]+'\n' for x in range(line, line+21)]
			h.writerow([file, " ".join(cut)])

for file in tqdm(file_list):
	try:
		getse(file)
	except:
		print("\n"+file)