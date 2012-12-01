from Bio import Entrez
from Bio import Medline
import csv
import re
from collections import Counter
import json
import string
from django.utils.encoding import smart_str
Entrez.email = "axfelix@gmail.com"

authors = []
authorfields = {}

with open("mcsneuro_authors.csv","r") as csvfile:
	authorreader = csv.reader(csvfile, delimiter=',')
	for row in authorreader:
		authors.append(row)

for x in authors:
	try:
		print x[0]
			
		handle = Entrez.esearch(db="pubmed", term=x[0])
		record = Entrez.read(handle)
		pmids = record["IdList"]

		handle = Entrez.efetch(db="pubmed", id=pmids, retmode="xml")
		records = Entrez.read(handle)
		records = list(records)

		meshterms = {}
		cnt = Counter()
		for y in records:
			scratch = open("mcs_scratch.txt","wb")
			scratch.write(str(y))
			scratch = open("mcs_scratch.txt","r")
			y = scratch.read()
			meshterms[y] = re.findall(r'(?<=DescriptorName\'\:\sStringElement\(\').+?(?=\')',smart_str(y))
			for z in meshterms[y]:
				cnt[z] += 1

		authorfields[str(x)] = dict(cnt)

	except:
		print ""

allterms = []	
for q,c in authorfields.iteritems():
	allterms.append(c.keys())
alltermslist = [item for sublist in allterms for item in sublist]
allterms = list(set(alltermslist))
	
with open("mcsneuro_mesh.csv","wb") as csvfile:
	meshwriter = csv.writer(csvfile, delimiter=',')
	meshwriter.writerow([''] + allterms)
	for q,c in authorfields.iteritems():
		meshwriter.writerow([q] + [c.get(w, 0) for w in allterms]) 