import sys
from ontCompare import alignGraphs, writeGraph




sourceFile = sys.argv[1]
targetFile = sys.argv[2]

availableMeasures = ["jaro", "jaro-winkler", "levenshtein", "string-equality", "uri-equality", "2-gram", "3-gram"]

propertiesString = input("Choose properties to compare (comma-separated) : ")

properties = [prop.strip() for prop in propertiesString.split(',')]

prop_sim_dict = {}

for prop in properties:
    inputValid = False
    while not inputValid:
        measuresString = input("Choose measures for property '{}' : ".format(prop))
        prop_sim_dict[prop] = [meas.strip() for meas in measuresString.split(',')]
        inputValid = True
        for measure in prop_sim_dict[prop]:
            if measure not in availableMeasures:
                inputValid = False
                print("Invalid measure :", measure)
                print("Available measures :", availableMeasures)

threshold = float(input("Choose threshold : "))
    
outputFile = input("Choose file to write alignment : ")


alignment = alignGraphs(sourceFile, targetFile, prop_sim_dict, threshold)

writeGraph(alignment, outputFile)



