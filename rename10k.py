import os
import re
import csv
from tqdm import tqdm

fileadd = "/Users/mengjiexu/Dropbox/edgar10k/8khtm"
file_list = os.listdir(fileadd)

for file in tqdm(file_list):
	new = file.replace(":","_").replace("/","_")
	oldname = "%s/%s"%(fileadd,file)
	newname = "%s/%s"%(fileadd,new)
	os.rename(oldname,newname) 

