import sys
import glob
import rdflib
import os

def getNIFEntities(gr):
	qres = gr.query(
	""" SELECT ?id ?mention ?start ?end ?verdict ?system ?gold
	WHERE {
		?id nif:anchorOf ?mention ;
		nif:beginIndex ?start ;
		nif:endIndex ?end ;
		<http://ilievski.nl/verdict> ?verdict ;
		<http://ilievski.nl/goldLink> ?gold ;
		<http://www.w3.org/2005/11/its/rdf#taIdentRef> ?system .
	} ORDER BY ?start""")
	return qres

w=open(sys.argv[1] + '.tsv', 'w')
os.chdir(sys.argv[1] + '/files')
#for resFile in glob.glob('res*.rdf'):
        #evalkey=str(counter)
counter=1
w.write('FILEID\tENTITYID\tSTART\tEND\tMENTION\tSYSTEM\tGOLD\tVERDICT\n')
while counter<=20:
	resFile="res" + str(counter) + ".rdf"
	g = rdflib.Graph()
	g.parse(resFile, format='n3')
	for row in getNIFEntities(g):
		w.write('%d\t%s\t%d\t%d\t%s\t%s\t%s\t%s\n' % (counter, str(row['id']), int(row['start']), int(row['end']), str(row['mention']), str('EMERGING ENTITY' if str(row['system']).startswith('http://vu.nl') else row['system']), str(row['gold'] if str(row['verdict'])=='false' else row['system']), str(row['verdict'])))
	counter+=1
w.close()

