from flask import jsonify, Flask, request, Response
from rdflib import Graph, URIRef
#from flask_cors import CORS, cross_origin
app = Flask(__name__)
#CORS(app)
import rdflib

def getTPs(gr):
	qres = gr.query(
	""" SELECT ?start ?end ?verdict ?ref ?conf ?gold
	WHERE {
		?id nif:beginIndex ?start ;
		nif:endIndex ?end ;
		<http://www.w3.org/2005/11/its/rdf#taIdentRef> ?ref ; 
		<http://ilievski.nl/verdict> ?verdict ;
		<http://ilievski.nl/goldLink> ?gold .
		OPTIONAL { ?id nif:confidence ?conf } 
	} ORDER BY DESC(?start)""")

	myList=[]
	for row in qres:
		myList.append([int(row['start']), int(row['end']), str(row['verdict']), str(row['ref']), float(row['conf'] or 1.0), str(row['gold'])])
	print(myList)
	return myList

@app.route("/<system>/<numFile>", methods = ['GET'])
def getNIFString(system, numFile):
	g=rdflib.Graph()
	g.parse(system + '/files/res' + numFile + '.rdf', format="n3")
	qres = g.query(
	""" SELECT ?s
	WHERE {
	?x nif:isString ?s
	} LIMIT 1
	""")
	
	tps=getTPs(g)

	for r in qres:
		response=jsonify({"s": r['s'].replace('\n\n','\n'), "tps": tps})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

if __name__ == "__main__":
	app.run()
