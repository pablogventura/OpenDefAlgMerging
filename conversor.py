from itertools import product, permutations


#covers = {0: {2, 3}, 1: set(), 2: {1}, 3: {1}}
n = 20
# cadenas:
covers = {e:{e+1} for e in range(n)}
covers[n-1] = set()

#covers[0] = set(range(n-1))
#covers = {e:{n-1} for e in range(1,n)}
#covers[n-1] = set()

lleq = dict(covers)

antes = dict()
while antes != lleq:
    antes = dict(lleq)
    for k in lleq:
        # print((lleq[k],k))
        lleq[k].add(k)
        for e in lleq[k]:
            lleq[k] = lleq[k].union(lleq[e])
#print (lleq)


def leq(a, b, D):
    return b in lleq[a]


def minimo(l, f):
    result = l[0]
    for e in l:
        if f(e, result, lleq):
            result = e
    return result


def maximo(l, f):
    result = l[0]
    for e in l:
        if f(result, e, lleq):
            result = e
    return result


def supremo(a, b, d):
    return minimo(list(d[a].intersection(d[b])), leq)


def infimo(a, b, f):
    menoresquea = {x for x in covers.keys() if f(x, a, lleq)}
    menoresqueb = {x for x in covers.keys() if f(x, b, lleq)}
    return maximo(list(menoresquea.intersection(menoresqueb)), leq)


print(" ".join(map(str, covers.keys())))
print("")
print("S 2")
for a, b in product(covers.keys(), repeat=2):
    print("%s %s %s" % (a, b, supremo(a, b, lleq)))
print("")
#print("E 3")
#for a, b, c in product(covers.keys(), repeat=3):
#    print("%s %s %s %s" % (a, b, c, supremo(a, b, lleq)))
print("")
print("I 2")
for a, b in product(covers.keys(), repeat=2):
    print("%s %s %s" % (a, b, infimo(a, b, leq)))
print("")
print("T0 %s 4" % len(list(permutations(covers.keys(), r=4))))
for t in permutations(covers.keys(), r=4):
    print(" ".join(map(str, t)))
print("")
