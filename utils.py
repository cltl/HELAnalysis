import rdflib

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


