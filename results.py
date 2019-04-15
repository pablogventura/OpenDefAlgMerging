import sys

from collections import defaultdict
# filename = sys.argv[1]
# f=open(filename,"r")
# f.readline() # asteriscos basura
# print(float(f.readline()[24:-5])) # hit
# print(float(f.readline()[24:-5]) # minion
# f.close()

import os

results = defaultdict(list)
files = [os.path.join(dp, f) for dp, dn, fn in os.walk("testing") for f in fn]
for i, f in enumerate(files):
    if f.endswith(".hvm"):
        
        _,dir,filename = f.split("/")
        file = open(f,"r")
        try:
            results[dir].append((float(file.readline()[9:-1]),float(file.readline()[9:-1])))
        except ValueError:
            print("ERROR in file %s" % f)

 
for k in results:
    value = (0,0)
    size = len(results[k])
    while results[k]:
        h,m=results[k].pop()
        value = (value[0]+h,value[1]+m)
    value = (value[0]/size,value[1]/size)
    results[k].append(value)
    print()
    print(k)
    print("Hit:    %s with %s samples" % (value[0],size))
    print("Minion: %s with %s samples" % (value[1], size))