from collections import defaultdict
import os
from functools import reduce # Valid in Python 2.6+, required in Python 3
import operator

results = defaultdict(list)
files = [os.path.join(dp, f) for dp, dn, fn in os.walk("testing/mega_hit_test") for f in fn]
for i, f in enumerate(files):
    if f.endswith(".megahit"):
        
        _,_,dir,filename = f.split("/")
        file = open(f,"r")
        try:
            counter=0
            while "*" not in file.readline():  # asteriscos basura
                counter+=1
                if counter>20:
                    raise ValueError
            file.readline() #definible
            if dir.endswith("boole"):
                s,_=filename.split("_", 1)
                size = 2**int(s)
            elif dir.endswith("alg_random"):
                s,_=filename.split("_", 1)
                size = int(s)
            elif dir.endswith("grupo_abeliano"):
                size = reduce(operator.mul,list( int(x) for x in filename.split("_"))[:-1],1)
            else:
                size = map(int,filename.split("_"))

            results[(dir,size)].append(float(file.readline()[14:]))
    
        except ValueError:
            print("ERROR in file %s" % f.replace(" ","\ "))
new_results = dict()
for k in results:
    value = 0
    size = len(results[k])
    while results[k]:
        h=results[k].pop()
        value = value+h
    value = value/size
    new_results[k]=value
    print()
    print(k)
    print("Time: %s" % value)
    
#
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# data = [(k,new_results[k][0],new_results[k][1]) for k in new_results]
#
# print(data)
#
# temp_data= sorted(data,key=lambda v:v[2])
# data=[]
# for n,h,m in temp_data:
#     if n == "ret":
#         data.append(("Distributive\nLattices",h,m))
#     elif n == "grupo_no_abeliano":
#         data.append(("Not Abelian\nGroups",h,m))
#     elif n == "grupo_abeliano":
#         data.append(("Abelian\nGroups",h,m))
#     elif n == "boole":
#         data.append(("Boolean\nAlgebras",h,m))
#     elif n == "alg_random":
#         data.append(("Random\nAlgebras",h,m))
#     else:
#         data.append((n, h, m))
#