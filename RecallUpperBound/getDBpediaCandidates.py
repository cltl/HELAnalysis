#!/usr/bin/python

# This script will take a CoNLL AIDA file as input 
# query it to DBpedia to check whether the correct candidate is returned at all 
# (upper bound recall measure) 
# author: marieke.van.erp@vu.nl
# date: 28 november 2016 

import sys
from time import sleep 
import urllib.parse 
import urllib.request
import json  

url = 'http://spotlight.sztaki.hu:2222/rest/candidates?text=President%20Obama'
#values = 'President%20Obama'
headers = {'Accept': 'application/json'}

def annotate(doc):
    query = doc
    urlPostPrefixSpotlight = "http://spotlight.sztaki.hu:2222/rest/candidates"
    args = urllib.parse.urlencode([("text", query), ("confidence", 0), ("support", 0)]).encode("utf-8")
    request = urllib.request.Request(urlPostPrefixSpotlight, data=args, headers={"Accept": "application/json"})
    response = urllib.request.urlopen(request).read()
    pydict= json.loads(response.decode('utf-8'))
    return pydict 
	

with open('AIDA-YAGO2-annotation-testb.tsv', 'r') as f:
	for line in f:
		line = line.rstrip()
		if 'DOCSTART' in line:
			continue
		if '-NME-' in line:
			continue 
		elements = line.split("\t")
		if len(elements) > 1:
			query = elements[1].replace("_", " ")
		else:
			continue 
		candidates = annotate(query)
		resultstring = elements[1] + "\t" + elements[2] + "\t" 
		try:
			for candidate in candidates['annotation']['surfaceForm']['resource']:
				resultstring = resultstring + 'http://en.wikipedia.org/wiki/' + candidate['@uri'] + "\t"
			print(resultstring) 
		except:
			print(resultstring, "NO DBPEDIA CANDIDATES")
		sleep(2) 



