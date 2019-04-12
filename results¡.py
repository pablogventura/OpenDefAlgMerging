import sys


filename = sys.argv[1]
f=open(filename,"r")
f.readline() # asteriscos basura
print(float(f.readline()[24:-5])) # hit
print(float(f.readline()[24:-5]) # minion
f.close()