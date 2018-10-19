from itertools import product




covers = {0:{1},1:{2},2:{1},3:{1}}
n=5
covers = {e:{e+1} for e in range(n)}
covers[n-1] = set()

lleq = dict(covers)

antes = dict()
while antes != lleq:
    antes = dict(lleq)
    for k in lleq:
        #print((lleq[k],k))
        lleq[k].add(k)
        for e in lleq[k]:
            lleq[k] = lleq[k].union(lleq[e])
#print (lleq)


def leq(a,b,D):
    return b in lleq[a]
    
def minimo(l,f):
    result = l[0]
    for e in l:
        if f(e,result,lleq):
            result = e
    return result
    
def maximo(l,f):
    result = l[0]
    for e in l:
        if f(result,e,lleq):
            result = e
    return result
    
def supremo(a,b,d):
    return minimo(list(d[a].intersection(d[b])),leq)
    
def infimo(a,b,d):
    return maximo(list(d[a].intersection(d[b])),leq)
    

for a,b in product(covers.keys(),repeat=2):
    print ("%s %s %s" % (a,b,supremo(a,b,lleq)))
