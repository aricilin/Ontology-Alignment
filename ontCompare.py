from rdflib.compare import to_isomorphic, graph_diff
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import OWL

from similarity import getSimFunction



def writeGraph(graph, outputFile, rdfFormat="nt"):
    graph.serialize(destination=outputFile, format=rdfFormat, encoding="utf-8")



def getPropertyURI(propertyString, graph):

    ns_prefix, prop = propertyString.split(":")
    for prefix, namespace in graph.namespaces():
        if prefix == ns_prefix:
            return (namespace + prop) 



def alignGraphs(sourceFile, targetFile, properties_similarities_dict, threshold):
    '''
    sourceFile : RDF source file
    targetFile : RDF target file
    properties : list of properties to compare
    similarities : list of similarity measures
    threshold : min similarity to declare two objects as the same

    '''

    source = Graph("default")
    source.open("store", create=True)
    source.parse(sourceFile,format="n3")

    target = Graph("default")
    target.open("store", create=True)
    target.parse(targetFile,format="n3")

    alignment = Graph("default")
    rejected = Graph("default")



    found_matches = 0
    rejected_matches = 0
    total_matches = 0

    for propertyString in properties_similarities_dict:

        predicate = getPropertyURI(propertyString, source)
        print(predicate)

        similarities = properties_similarities_dict[propertyString]
        print(similarities)

        for source_s in source.subjects(predicate, None):

            if isinstance(source_s, BNode):
                continue
            
            for target_s in target.subjects(predicate, None):

                if isinstance(target_s, BNode):
                    continue
                
                if (source_s, OWL.differentFrom, target_s) in rejected:
                    continue

                source_o_list = [obj for obj in source.objects(source_s, predicate) if isinstance(obj, (Literal, URIRef))]
                target_o_list = [obj for obj in target.objects(target_s, predicate) if isinstance(obj, (Literal, URIRef))]

                if len(source_o_list) == 0 or len(target_o_list) == 0:
                    continue

                sim_values = []
                
                for source_o in source_o_list:
                    for target_o in target_o_list:
                        sim_values.append(compare(source_o, target_o, similarities))
            
                if(len(sim_values) > 0):
                    if max(sim_values) > threshold:
                        if (source_s, OWL.sameAs, target_s) not in alignment:
                            alignment.add((source_s, OWL.sameAs, target_s))
                            #print("Found match : ", source_s, " ||| ",  target_s)
                            #print("Matched values : ", source_o_list, " ||| ", target_o_list)
                            found_matches += 1
                            total_matches += 1
                            #print("Found", found_matches, ", rejected", rejected_matches, ", remaining", total_matches, end='\r')
                    else:
                        if (source_s, OWL.differentFrom, target_s) not in rejected:
                            rejected.add((source_s, OWL.differentFrom, target_s))
                        if (source_s, OWL.sameAs, target_s) in alignment:
                            alignment.remove((source_s, OWL.sameAs, target_s))
                            rejected_matches += 1
                            total_matches -= 1
                            #print("Found", found_matches, ", rejected", rejected_matches, ", remaining", total_matches, end='\r')
                            print("Rejected", source_o_list, "||" , target_o_list)

    return alignment



def compare(object_1, object_2, similarities):

    sim_values = []

    

    for simString in similarities:
        if simString == "uri-equality":
            str_1 = object_1.n3()
            str_2 = object_2.n3()
        else:
            str_1 = str(object_1)
            str_2 = str(object_2)
        sim = getSimFunction(simString)
        sim_values.append(sim(str_1, str_2))

    return (sum(sim_values)/len(sim_values))









