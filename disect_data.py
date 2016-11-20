import json
import os
from collections import OrderedDict,defaultdict
from ast import literal_eval as make_tuple
import pickle
import rdflib
import sys
import glob

def getNIFString(gr):
        qres = gr.query(
        """ SELECT ?s
        WHERE {
                ?x nif:isString ?s
        } LIMIT 1
        """)
        for r in qres:
                return r['s']

def insertEvaluation(gr, startid, verdict, links, wrongLinks=None):
	#print(json.dumps(links))

	#qres = gr.update(""" INSERT { ?id <http://ilievski.nl/verdict> """ + verdict  + """ } WHERE
#	gr.update(""" DELETE { ?id <http://www.w3.org/2005/11/its/rdf#taIdentRef> ?q } WHERE
#        { ?id <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#beginIndex> \"""" + str(startid) + """\"^^xsd:nonNegativeInteger ; <http://www.w3.org/2005/11/its/rdf#taIdentRef> ?q }""")

	print(len(gr))
	s=""
	if type(links) is list: #not links.startswith("http://vu.nl"):
		for l in links:
			s+= "<http://ilievski.nl/goldLink> <" + l + "> ; "
	else:
		s="<http://ilievski.nl/goldLink> <http://vu.nl/unknown> ; "

	if wrongLinks:
		print("Wrong links ", verdict, links, wrongLinks)
		gr.update(""" INSERT { ?id <http://ilievski.nl/verdict> """ + verdict  + """ ; """ + s.strip('; ')  + """ } WHERE
	{ ?id <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#beginIndex> \"""" + str(startid) + """\"^^xsd:nonNegativeInteger . } """)
	else:
		gr.update(""" INSERT { ?id <http://ilievski.nl/verdict> """ + verdict  + """ ; """ + s.strip('; ') + """ } WHERE
        { ?id <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#beginIndex> \"""" + str(startid) + """\"^^xsd:nonNegativeInteger . } """)
	print(len(gr))

def getGoodLinks(a):
	links=[]
	for link in a:
		#if link.startswith("http://wikidata") or link.startswith("http://dbpedia.org") or link.startswith("http://en.wikipedia.org"):
		if ("wikidata.org" in link or "wikipedia.org" in link or "dbpedia.org" in link) and "disambiguation" not in link:#.startswith("http://wikidata"):
			links.append(link.strip())
	if len(links):
		return links
	else:
		return "EMERGING ENTITY"

def getTuple(x):
	splitter=x.split(', [')
	nums=splitter[0].strip('(').split(',')
	links=getGoodLinks(splitter[1].split(','))
	nums.append(links)
	return nums

def obtainFromLine(line, which):
	tupley = line.strip().lstrip(which + ': ')
	t=getTuple(tupley)
	return t

if sys.argv[1]=='hel':
	os.chdir('HEL')
	firstIterationFile='hel.txt'
	print("HEL")
else:
	os.chdir('AGDISTIS')
	firstIterationFile='agdistis.txt'

data=open(firstIterationFile, 'r')
tp=defaultdict(str)
fn=defaultdict(str)
fp=defaultdict(str)
incorrect=defaultdict(str)
goodLinks=defaultdict(str)
wrongLinks=defaultdict(str)
allLinks=defaultdict(str)
for line in data:
	if line.startswith('DOCUMENT '):
		currentDoc=line.strip().replace('DOCUMENT ','')
		#if len(currentDoc)<2:
		#	currentDoc = '0' + currentDoc
		tp[currentDoc]=set()
		fp[currentDoc]=set()
		fn[currentDoc]=set()
	elif line.startswith('TP: '):
                lineData=obtainFromLine(line, 'TP')
                tp[currentDoc].add(lineData[0])
                links=lineData[2]
                try:
                        goodLinks[currentDoc][str(lineData[0])]=links
                except:
                        goodLinks[currentDoc]={str(lineData[0]):links}
	elif line.startswith('FN: '):
		lineData=obtainFromLine(line, 'FN')
		fn[currentDoc].add(lineData[0])
		links=lineData[2]
		try:
			allLinks[currentDoc][str(lineData[0])]=links
		except:
			allLinks[currentDoc]={str(lineData[0]):links}
	elif line.startswith('FP: '):
                lineData=obtainFromLine(line, 'FP')
                fp[currentDoc].add(lineData[0])
                links=lineData[2]
                try:
                        wrongLinks[currentDoc][str(lineData[0])]=links
                except:
                        wrongLinks[currentDoc]={str(lineData[0]):links}

                #startend, link=getStartEndLink(line)
                #links[startend]={'gold': link}

s=0


#print('fp', sorted(list(fp["00"])))
#print('diff', fp["00"].difference(tp["00"]))
for k in fn:
	incorrect[k]=fp[k].difference(tp[k])
#for k in sorted(fn):
#	s+=len(fn[k])
	#print(k, sorted(list(tp[k])))

#print('incorrect', sorted(list(incorrect["00"])))
#pickle.dump(tp, open("correct.p", "wb"))
#pickle.dump(incorrect, open("incorrect.p", "wb"))
#print("Pickles stored")

#HEL=open("lastRun.log", "r")

#g.parse("res1.rdf", format="n3")


for resFile in glob.glob('res*.rdf'):
	#evalkey=str(counter)
	g = rdflib.Graph()
	g.parse(resFile, format='n3')
	counter=str(int(resFile.lstrip('res').rstrip('.rdf'))-1)

	print("File " + counter)
	for startid in tp[counter]:
		insertEvaluation(g, startid, "True", goodLinks[counter][startid])
	for startid in incorrect[counter]:

		if startid in wrongLinks[counter]:
			insertEvaluation(g, startid, "False", allLinks[counter][startid], wrongLinks[counter][startid])
		else:
			insertEvaluation(g, startid, "False", allLinks[counter][startid])
			print(startid, " not in ",wrongLinks[counter])

	g.serialize(destination="files/" + resFile, format="n3")
