from token import EQUAL
import rdflib
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QMessageBox, QInputDialog
from rdflib.compare import to_isomorphic, graph_diff
from rdflib import Graph, URIRef

#graph = rdflib.Graph("default")
#graph.open("store", create=True)
#graph.parse("resDHT.rdf.txt",format="xml")

# print out all the triples in the graph
#for subject, predicate, object in graph:
 #   print (subject, predicate, object)

total: float = 0
true_positive: float = 0
false_positive: float = 0
false_negative: float = 0


sourceFile = sys.argv[1]
referenceFile = sys.argv[2]


source = rdflib.Graph("default")
source.open("store", create=True)
source.parse(sourceFile,format="nt")
ref = rdflib.Graph("default")
ref.open("store", create=True)
ref.parse(referenceFile, format="nt")

iso_source = to_isomorphic(source)
iso_ref = to_isomorphic(ref)
in_both, only_in_first, only_in_second = graph_diff(iso_source, iso_ref)
values1 = set()
values2 = set()

for s, p, o in in_both:
    total += 1
    true_positive+=1    
    #print(s, p, o)

for s, p, o in only_in_first:
    total += 1
    false_positive += 1

for s, p, o in only_in_second:
    total += 1
    false_negative += 1


precision:float = true_positive/(true_positive+false_positive)
recall:float = true_positive/(true_positive+false_negative)
fmeasure:float = (2*precision*recall)/(precision+recall)


#print("vrai/total :" , true_positive/total)
#print ("erreur de niveau 2 : " , false_negative/total)
#print ("erreur de niveau 1 : ", false_positive/total)
print("precision :", precision)
print("recall :", recall)
print("f-measure :" , fmeasure)

