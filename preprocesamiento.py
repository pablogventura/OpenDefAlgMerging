from collections import defaultdict

def quotient(s,f):
    #cociente del conjunto s, por la funcion f
    result = {e:[e] for e in s}
    for a in s:
        if a not in result:
            continue
        for b in s:
            if b not in result or a==b:
                continue
            if f(b)==f(a):
                result[a]+=result[b]
                del result[b]
    return result
    
def patron(t):
    #cociente del conjunto s, por la funcion f
    result = defaultdict(set)
    for i,a in enumerate(t):
        result[a].add(i)
    return set(frozenset(s) for s in result.values())
    
def preprocesamiento(T):
    result = []
    q = quotient([(1,2,3),(1,2,4),(1,2,2),(2,1,1),(1,1,2)],patron).values()
    for r in q:
        result.append(set())
        for t in r:
            result[-1].add(tuple(sorted(set(t))))#esto esta mal, tiene que borrar solo el que es igual
    return result
