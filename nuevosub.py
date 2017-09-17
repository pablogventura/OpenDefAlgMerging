from itertools import product
from collections import defaultdict


def tipoSub(alpha,Func,debug=True):
    #input alpha, Func
    alpha=list(sorted(alpha))
    H=[alpha]
    i = len(alpha)
    T = defaultdict(set,{a:{i} for i,a in enumerate(alpha)})
    O = H[-1]
    
    while O:
        H.append([])
        for ar in sorted(Func):
            for tup in TupAd(H,ar):
                for f in Func[ar]:
                    x=f(*tup)
                    if any(x in h for h in H):
                        T[x].add(i)
                    else:
                        T[x].add(i)
                        H[-1].append(x)
                    i+=1 #faltaba en el algoritmo original
        O = H[-1]
    if debug:
        print tuple(len(h) for h in H),sorted(tuple(len(T[k]) for k in sorted(T.keys())))
    else:
        return H,T

def TupAd(h,k):
    #devuelve una tupla de largo k con por lo menos un obligatorio
    # que estan en el penultimo lugar de h
    
    flath=[item for sublist in h for item in sublist]
    #print flath
    o=h[-2]
    
    for tup in product(flath,repeat=k):
        if any(t in o for t in tup):
            yield tup

def join(a,b):
    if a==1 or b==1:
        return 1
    elif a==0:
        return b
    elif b==0:
        return a
    return 1

