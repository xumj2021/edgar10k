from lxml import etree
import csv, re, os
from tqdm import tqdm

fileadd = "/Users/mengjiexu/Dropbox/edgar10k/10khtm/"
os.chdir(fileadd)
filelist = os.listdir(fileadd)

def trans(element):
	text = str(etree.tostring(element))
	return(text)

def find_position(root, element):
	textlist = []
	line_number = 0
	pos = 0

	for child in root.iter():
		textlist.append(child.text.replace("\n"," ").replace("\xa0", " "))

		line_number += 1
		if element == child:
			pos = line_number
	
	return([pos, textlist])

def getend(core, target):
	iternum = 1
	if target.index(core) < len(target)-1:
		endelement = target[int(target.index(core))+iternum]
		if endelement.text:
			while (not re.findall("[a-zA-Z]+", str(endelement.text))) or len(endelement.text)<5:
				iternum += 1
				endelement = target[int(target.index(core))+iternum]
	else:
		endelement = core

	return(endelement)

def getsibling(page, core):

	[tag, attr] = [core.tag, core.attrib]

	values = " ".join(attr.values())

	parent = 0
	tag0 = ""
	if re.findall("nonnumeric|http|em", tag.lower()) and not re.findall("bold", values):
		tag0 = tag
		core = core.getparent()
		[tag, attr] = [core.tag, core.attrib]
		parent = 1

	con = ""

	for key, value in attr.items():
		con = con + "contains(@%s, \"%s\")"%(key, value) + " and "

	con = con[:-5]		

	if parent == 1:
		addp = "/%s"%tag0
	else:
		addp = ""

	if con != "" :    
		path = "//%s[%s]"%(tag, con) + addp
	else:
		path = "//%s"%tag + addp

	target = page.xpath("%s"%path)

	if parent == 1:
		target = [i.getparent() for i in target]

	endelement = getend(core, target)

	return([endelement, path, parent])

def getbackendpos(page, startpos, maxpos):

	backendpos = min(startpos +100, maxpos)

	line_number = 0
	elist = [i for i in page.iter()]
	endelement = elist[maxpos]

	for j in range(startpos+1, maxpos+1):
		if re.findall("<b>|<i>|bold|italic|font-weight:700", trans(elist[j])):
			backendpos = j
			endelement = elist[j]
			break

	return([backendpos, endelement])

def getsetext(file):
	try:
		page = etree.HTML(open(file,'r').read())
	except:
		page = etree.parse(file)

	for i in page.iter():

		if not i.text:
			i.text = ""

		if len(i) > 1:
			try:
				i.text = i.text + "".join(i.itertext())
			except:
				pass

		if i.tail:
			if re.findall("[a-zA-Z]+", str(i.tail)):
				i.text = i.tail

		tag = str(i.tag)
		if re.findall("}|nonnumeric|http", tag.lower()):
			i.tag = tag.split("}")[-1]

	pool = page.xpath(".//*[contains(text(), 'SUBSEQUENT EVENT') or contains(text(), 'Subsequent Event')]")

	core = ""
	for candi in pool:
		if (re.findall("bold|<b>|<i>|ote|italic|font-weight:700", trans(candi)) or re.findall("bold|<b>|<i>|ote|italic|font-weight:700", trans(candi.getparent()))) and not (re.findall("see|See",candi.text)):
			core = candi

	if core == "":
		core = pool[-1]

	root = core.getroottree()

	[startpos, textlist] = find_position(root, core)
	[endelement, path, parent] = getsibling(root, core)

	if parent == 1:
		core = core.getparent()

	maxpos = len(textlist) - 1

	backpos = 0
	isendnode = 0
	if endelement != core:
		[endpos, textlist] = find_position(root, endelement)
		if endpos - startpos > 100:
			[endpos, endelement] = getbackendpos(root, startpos, maxpos)
			backpos = 1
	else:
		[endpos, endelement] = getbackendpos(root, startpos, maxpos)
		backpos = 1
		isendnode = 1

	elist = [i for i in page.iter()]

	with open("/Users/mengjiexu/Dropbox/edgar10k/10kbody/body_%s.txt"%file[:-4], 'a') as l:
		for k in range(startpos, endpos+1):
			l.write("Line %s : "%k + trans(elist[k]) + "\n\n")


	setext = " ".join(textlist[startpos: endpos+1])
	keyargs = [file, startpos, endpos, path, backpos, isendnode, core.text, endelement.text, setext]

	with open("/Users/mengjiexu/Dropbox/edgar10k/10ksetext/setext_%s.txt"%file[:-4], 'a') as p:
		p.write(setext)

	with open("/Users/mengjiexu/Dropbox/edgar10k/10kseargs.csv", 'a') as b:
		c = csv.writer(b)
		c.writerow(keyargs)


with open("/Users/mengjiexu/Dropbox/edgar10k/exceptions.txt", 'a') as m:
	for file in tqdm(filelist):
		try:
			getsetext(file)
		except:
			m.write(file + "\n")
