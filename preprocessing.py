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

def limpia(t):
    result=set()
    for e in t:
        result.add(t.index(e))
    return sorted(result)


def preprocesamiento(T):
    result = []
    q = quotient(T,patron)
    for p in q:
        indices=limpia(p)
        result.append(set())
        for t in q[p]:
            result[-1].add(tuple(t[i] for i in indices))
    return result
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
