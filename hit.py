from itertools import product
from collections import defaultdict

def tuple_number(t,order):
    flath = [item for sublist in order for item in sublist]
    return tuple(flath.index(e) for e in t)


def hit(model, alpha):
    # input model, alpha
    alpha = list(sorted(alpha))
    ops = model.operations
    H = [alpha]
    i = len(alpha)
    T = defaultdict(set, {a:{(len(H)-1,-1,(i,))}  for i, a in enumerate(alpha)})
    O = H[-1]

    while O:
        H.append([])
        for ar in sorted(ops):
            for tup in TupAd(H, ar):
                i += 1  
                for sym_i,f in enumerate(sorted(ops[ar],key=lambda f:f[0])):
                    f=f[1]
                    x = f(*tup)
                    if any(x in h for h in H):
                        T[x].add((i,sym_i,tuple_number(tup,H)))
                    else:
                        T[x].add((i,sym_i,tuple_number(tup,H)))
                        H[-1].append(x)
            i = 0
        O = H[-1]
    return H, T


def TupAd(h, k):
    # devuelve una tupla de largo k con por lo menos un obligatorio
    # que estan en el penultimo lugar de h

    flath = [item for sublist in h for item in sublist]
    # print flath
    o = h[-2]

    for tup in product(flath, repeat=k):
        if any(t in o for t in tup):
            yield tup

