import re
import sys


inputFile = open(sys.argv[1], "r")
outputFile = open(sys.argv[2], "w")



while True:
    line1 = inputFile.readline()
    if not line1:
        break

    entity1_match = re.match("^<entity1 rdf:resource=\"(.*)\"/>$", line1)
    if entity1_match:
        entity1 = entity1_match.group(1)
        line2 = inputFile.readline()
        entity2_match = re.match("^<entity2 rdf:resource=\"(.*)\"/>$", line2)
        if entity2_match:
            entity2 = entity2_match.group(1)
            newline = "<{}> <http://www.w3.org/2002/07/owl#sameAs> <{}> .\n".format(entity1, entity2)
            outputFile.write(newline)

        else:
            print("ERROR : entity 1 found, but not 2")
            break

inputFile.close()
outputFile.close()

