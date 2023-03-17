import re

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
            if (pair_strength < -5):
                holder = interests.string.split(",")
                holder[2] = "very low)"
                print(", ".join(holder))
            elif (pair_strength >= -5 and pair_strength < 0):
                holder = interests.string.split(",")
                holder[2] = "low)"
                print(", ".join(holder))
            elif (pair_strength == 0):
                holder = interests.string.split(",")
                holder[2] = "neutral)"
                print(", ".join(holder))
            elif (pair_strength > 0 and pair_strength <= 5):
                holder = interests.string.split(",")
                holder[2] = "high)"
                print(", ".join(holder))
            elif (pair_strength > 5):
                holder = interests.string.split(",")
                holder[2] = "very high)"
                print(", ".join(holder))
        elif (facets):
            pair_strength = int(facets.string.split(",")[2][:-1])
            if (pair_strength < -5):
                holder = facets.string.split(",")
                holder[2] = "very low)"
                print(", ".join(holder))
            elif (pair_strength >= -5 and pair_strength < 0):
                holder = facets.string.split(",")
                holder[2] = "low)"
                print(", ".join(holder))
            elif (pair_strength == 0):
                holder = facets.string.split(",")
                holder[2] = "neutral)"
                print(", ".join(holder))
            elif (pair_strength > 0 and pair_strength <= 5):
                holder = facets.string.split(",")
                holder[2] = "high)"
                print(", ".join(holder))
            elif (pair_strength > 5):
                holder = facets.string.split(",")
                holder[2] = "very high)"
                print(", ".join(holder))
        elif (similarity):
            pair_strength = int(similarity.string.split(",")[2][:-1])
            if (pair_strength < -5):
                holder = similarity.string.split(",")
                holder[2] = "very low)"
                print(", ".join(holder))
            elif (pair_strength >= -5 and pair_strength < 0):
                holder = similarity.string.split(",")
                holder[2] = "low)"
                print(", ".join(holder))
            elif (pair_strength == 0):
                holder = similarity.string.split(",")
                holder[2] = "neutral)"
                print(", ".join(holder))
            elif (pair_strength > 0 and pair_strength <= 5):
                holder = similarity.string.split(",")
                holder[2] = "high)"
                print(", ".join(holder))
            elif (pair_strength > 5):
                holder = similarity.string.split(",")
                holder[2] = "very high)"
                print(", ".join(holder))
        elif (affinity):
            pair_strength = int(affinity.string.split(",")[2][:-1])
            if (pair_strength < -5):
                holder = affinity.string.split(",")
                holder[2] = "very low)"
                print(", ".join(holder))
            elif (pair_strength >= -5 and pair_strength < 0):
                holder = affinity.string.split(",")
                holder[2] = "low)"
                print(", ".join(holder))
            elif (pair_strength == 0):
                holder = affinity.string.split(",")
                holder[2] = "neutral)"
                print(", ".join(holder))
            elif (pair_strength > 0 and pair_strength <= 5):
                holder = affinity.string.split(",")
                holder[2] = "high)"
                print(", ".join(holder))
            elif (pair_strength > 5):
                holder = affinity.string.split(",")
                holder[2] = "very high)"
                print(", ".join(holder))
            
    
    
    
    
    
    
    
    file.close()