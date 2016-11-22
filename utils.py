import rdflib
import json, sys, pandas

def getCount(q, resFile):
	g = rdflib.Graph()
	g.parse(resFile, format='n3')
	qres=g.query(q)
	for row in qres:
		return int(row[0])

def countCandidates(resFile):
	g = rdflib.Graph()
	g.parse(resFile, format='n3')
	q="SELECT ?ent (count(distinct(?candidate)) as ?cnt) WHERE { ?ent a nif:Phrase . OPTIONAL { ?ent <http://ilievski.nl/candidate> ?candidate } } GROUP BY ?ent"
	qres=g.query(q)
	s=0
	for row in qres:
		s+=int(row[1])
	return s, len(qres)

def recallOfCandidates(resFile):
	q="SELECT (count(DISTINCT(?ent)) as ?countEntities) WHERE { ?ent a nif:Phrase . FILTER NOT EXISTS { ?ent <http://ilievski.nl/goldLink> <http://vu.nl/unknown> } . FILTER EXISTS { ?ent <http://ilievski.nl/goldLink> ?candidate ; <http://ilievski.nl/candidate> ?candidate } }"
	return getCount(q, resFile)

def NILmentions(resFile):
	q="SELECT (count(?ent) as ?countEntities) WHERE { ?ent a nif:Phrase ; <http://ilievski.nl/goldLink> <http://vu.nl/unknown> }"
	return getCount(q, resFile)

def NILmentionsNoCands(resFile):
	query="SELECT (count(DISTINCT(?ent)) as ?countEntities) WHERE { ?ent a nif:Phrase ; <http://ilievski.nl/goldLink> <http://vu.nl/unknown> . FILTER NOT EXISTS { ?ent <http://ilievski.nl/candidate> ?cand } }"
	return getCount(query, resFile)

def inspectFile(inspectMe):
	g=rdflib.Graph()
	g.parse(inspectMe, format='n3')
	q="SELECT ?ent ?ment ?candscores WHERE { ?ent <http://ilievski.nl/candidatescores> ?candscores ; nif:anchorOf ?ment } ORDER BY ?ent"
	qres=g.query(q)
	headers = ['candidate', 'strSim', 'semCoh', 'topK', 'recency', 'tmpPop', 'SCORE']
	pandas.set_option('display.max_columns', None)

	precision=3
	data=[]
	entity=""
	for row in qres:
		if entity=="":
			entity=row[0]
			print()
			print(row[1])
		elif entity!=row[0]:
			df2 = pandas.DataFrame(data, columns=headers)
			with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
				print(df2.sort_values('SCORE', 0, False).head(50).to_string())
			print()
			print(row[1])
			data=[]
			entity=row[0]
		jsonCand=json.loads(row[2])
		for c in jsonCand:
			data.append([c, round(jsonCand[c][0],precision) ,round(jsonCand[c][1], precision),round(jsonCand[c][2],3),round(jsonCand[c][3], 3),round(jsonCand[c][4],3),round(jsonCand[c][5],3) ])
