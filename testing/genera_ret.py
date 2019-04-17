from itertools import product
from random import sample
import sys


def join(a, b):
    # supremo
    return a | b


def meet(a, b):
    # infimo
    return a & b


def closure(ancho,muestra,q=None):
    generators = sample(range(2 ** ancho), muestra)
    news = set(generators)
    universe = set()
    rel_meet = set()
    rel_join = set()
    while news:
        local_news = set()
        for t in product(news, news):
            local_news.add(join(*t))
            local_news.add(meet(*t))
            rel_join.add(t+(join(*t),))
            rel_meet.add(t+(meet(*t),))
        for t in product(news, universe):
            local_news.add(join(*t))
            local_news.add(meet(*t))
            rel_join.add(t+(join(*t),))
            rel_meet.add(t+(meet(*t),))
        for t in product(universe, news):
            local_news.add(join(*t))
            local_news.add(meet(*t))
            rel_join.add(t+(join(*t),))
            rel_meet.add(t+(meet(*t),))

        local_news -= universe
        local_news -= news
        universe |= news
        news = set(local_news)
        if (q and (len(universe) > q) or (q and (not news and len(universe)<q))):
            print("intento")
            generators = sample(range(2 ** ancho), muestra)
            news = set(generators)
            universe = set()
            rel_meet = set()
            rel_join = set()
    print(" ".join(map(str, universe)))
    print("# Universe Size: %s" % len(universe))
    print("# Generated from: " + " ".join(map(str, generators)))
    print("")
    print("m 2")
    for a, b, r in rel_meet:
        print("%s %s %s" % (a, b, r))
    print("")
    print("j 2")
    for a, b, r in rel_join:
        print("%s %s %s" % (a, b, r))
    print("T0 %s 2" % len(universe)**2)
    for a, b in product(universe, universe):
        print("%s %s" % (a, b))


def main():
    try:
        ancho = int(sys.argv[1])
    except:
        print("Toma un numero de ancho de las tuplas,")
        print("y un numero opcional de muestras, para generar un ret distributivo")
        print("sino genera un algebra de boole")
        sys.exit(1)
    try:
        muestra = int(sys.argv[2])
    except:
        muestra = 2**ancho
    try:
        q = int(sys.argv[3])
    except:
        q = None
    closure(ancho,muestra,q)


if __name__ == "__main__":
    main()
