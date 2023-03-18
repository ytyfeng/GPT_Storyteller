import re
import sys


def print_to_stderr(*a):
    print(*a, file=sys.stderr)
    
    
#"Enter output file name: "
input_file = input()

with open(input_file) as file:
    #print(file.read())
    skip = file.readline()
    skip = file.readline()
    skip = file.readline()
    skip = file.readline()
    actual_line = file.readline()
    trying = actual_line.split(" ")
    trying[-1] = trying[-1][:-1]
    #print(trying[-1])
    for section in trying:
        interests = re.search("pair_interest_similarity(.*,.*,.*)\Z", section)
        facets = re.search("pair_facet_similarity(.*,.*,.*)\Z", section)
        similarity = re.search("pair_similarity(.*,.*,.*)\Z", section)
        affinity = re.search("pair_affinity(.*,.*,.*)\Z", section)
        if (interests):
            #print(interests.string)
            pair_strength = int(interests.string.split(",")[2][:-1])
            #print(interests.string + " and " + str(pair_strength))
            #print_to_stderr(interests.string.split(",")[0][25::])
            #print_to_stderr(interests.string.split(",")[1])
            if (pair_strength < -5):
                holder = interests.string.split(",")
                holder[2] = "very low)"
                #print(", ".join(holder))
                print(interests.string.split(",")[0][25::] + " has very few similar interests with " + interests.string.split(",")[1])
            elif (pair_strength >= -5 and pair_strength < 0):
                holder = interests.string.split(",")
                holder[2] = "low)"
                #print(", ".join(holder))
                print(interests.string.split(",")[0][25::] + " has few similar interests with " + interests.string.split(",")[1])
            elif (pair_strength == 0):
                holder = interests.string.split(",")
                holder[2] = "neutral)"
                #print(", ".join(holder))
                #print(interests.string.split(",")[0][25::] + " has few similar interests with " + interests.string.split(",")[1])
            elif (pair_strength > 0 and pair_strength <= 5):
                holder = interests.string.split(",")
                holder[2] = "high)"
                #print(", ".join(holder))
                print(interests.string.split(",")[0][25::] + " has some similar interests with " + interests.string.split(",")[1])
            elif (pair_strength > 5):
                holder = interests.string.split(",")
                holder[2] = "very high)"
                #print(", ".join(holder))
                print(interests.string.split(",")[0][25::] + " has many similar interests with " + interests.string.split(",")[1])
        elif (facets):
            pair_strength = int(facets.string.split(",")[2][:-1])
            #print_to_stderr(facets.string.split(",")[0][22::])
            if (pair_strength < -5):
                holder = facets.string.split(",")
                holder[2] = "very low)"
                #print(", ".join(holder))
                print(facets.string.split(",")[0][22::] + " has very few shared facets with " + facets.string.split(",")[1])
            elif (pair_strength >= -5 and pair_strength < 0):
                holder = facets.string.split(",")
                holder[2] = "low)"
                #print(", ".join(holder))
                print(facets.string.split(",")[0][22::] + " has few shared facets with " + facets.string.split(",")[1])
            elif (pair_strength == 0):
                holder = facets.string.split(",")
                holder[2] = "neutral)"
                #print(", ".join(holder))
                #print(facets.string.split(",")[0][22::] + " has few shared facets with " + facets.string.split(",")[1])
            elif (pair_strength > 0 and pair_strength <= 5):
                holder = facets.string.split(",")
                holder[2] = "high)"
                #print(", ".join(holder))
                print(facets.string.split(",")[0][22::] + " has some shared facets with " + facets.string.split(",")[1])
            elif (pair_strength > 5):
                holder = facets.string.split(",")
                holder[2] = "very high)"
                #print(", ".join(holder))
                print(facets.string.split(",")[0][22::] + " has many shared facets with " + facets.string.split(",")[1])
        elif (similarity):
            pair_strength = int(similarity.string.split(",")[2][:-1])
            #print_to_stderr(similarity.string.split(",")[0][16::])
            if (pair_strength < -5):
                holder = similarity.string.split(",")
                holder[2] = "very low)"
                #print(", ".join(holder))
                print(similarity.string.split(",")[0][16::] + " has very low similarity with " + similarity.string.split(",")[1])
            elif (pair_strength >= -5 and pair_strength < 0):
                holder = similarity.string.split(",")
                holder[2] = "low)"
                #print(", ".join(holder))
                print(similarity.string.split(",")[0][16::] + " has low similarity with " + similarity.string.split(",")[1])
            elif (pair_strength == 0):
                holder = similarity.string.split(",")
                holder[2] = "neutral)"
                #print(", ".join(holder))
                #print(similarity.string.split(",")[0][16::] + " has some similarity with " + similarity.string.split(",")[1])
            elif (pair_strength > 0 and pair_strength <= 5):
                holder = similarity.string.split(",")
                holder[2] = "high)"
                #print(", ".join(holder))
                print(similarity.string.split(",")[0][16::] + " has high similarity with " + similarity.string.split(",")[1])
            elif (pair_strength > 5):
                holder = similarity.string.split(",")
                holder[2] = "very high)"
                #print(", ".join(holder))
                print(similarity.string.split(",")[0][16::] + " has very high similarity with " + similarity.string.split(",")[1])
        elif (affinity):
            pair_strength = int(affinity.string.split(",")[2][:-1])
            #print_to_stderr(affinity.string.split(",")[0][14::])
            if (pair_strength < -5):
                holder = affinity.string.split(",")
                holder[2] = "very low)"
                #print(", ".join(holder))
                print(affinity.string.split(",")[0][14::] + " has very low affinity with " + affinity.string.split(",")[1])
            elif (pair_strength >= -5 and pair_strength < 0):
                holder = affinity.string.split(",")
                holder[2] = "low)"
                #print(", ".join(holder))
                print(affinity.string.split(",")[0][14::] + " has low affinity with " + affinity.string.split(",")[1])
            elif (pair_strength == 0):
                holder = affinity.string.split(",")
                holder[2] = "neutral)"
                #print(", ".join(holder))
                #print(affinity.string.split(",")[0][14::] + " has some affinity with " + affinity.string.split(",")[1])
            elif (pair_strength > 0 and pair_strength <= 5):
                holder = affinity.string.split(",")
                holder[2] = "high)"
                #print(", ".join(holder))
                print(affinity.string.split(",")[0][14::] + " has high affinity with " + affinity.string.split(",")[1])
            elif (pair_strength > 5):
                holder = affinity.string.split(",")
                holder[2] = "very high)"
                #print(", ".join(holder))
                print(affinity.string.split(",")[0][14::] + " has very high affinity with " + affinity.string.split(",")[1])
            
    
    
    
    
    
    
    
    file.close()