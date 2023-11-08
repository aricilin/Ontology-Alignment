from math import floor, ceil
from strsimpy.jaro_winkler import JaroWinkler
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from strsimpy.cosine import Cosine





def jaro(s1, s2):
     
    if (s1 == s2):
        return 1.0
 
    len1 = len(s1)
    len2 = len(s2)
    max_dist = floor(max(len1, len2) / 2) - 1
    match = 0
    hash_s1 = [0] * len(s1)
    hash_s2 = [0] * len(s2)
 
    for i in range(len1):
 
        for j in range(max(0, i - max_dist),
                       min(len2, i + max_dist + 1)):

            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break

    if (match == 0):
        return 0.0

    t = 0
    point = 0

    for i in range(len1):
        if (hash_s1[i]):
            while (hash_s2[point] == 0):
                point += 1
 
            if (s1[i] != s2[point]):
                t += 1
            point += 1
    t = t//2

    return (match/ len1 + match / len2 + (match - t) / match)/ 3.0



def getSimFunction(simString):
    match simString:

        case "string-equality":
            return (lambda s1, s2: (1 if s1 == s2 else 0))

        case "num-equality":
            return (lambda s1, s2: (1 if float(s1) == float(s2) else 0))

        case "uri-equality":
            return (lambda s1, s2: (1 if s1 == s2 else 0))

        case "jaro":
            return jaro

        case "jaro-winkler":
            jarowinkler = JaroWinkler()
            return jarowinkler.similarity

        case "levenshtein":
            levenshtein_norm = NormalizedLevenshtein()
            return levenshtein_norm.similarity
        
        case "2-gram":
            cosine2 = Cosine(2)
            return cosine2.similarity

        case "3-gram":
            cosine3 = Cosine(3)
            return cosine3.similarity



         


