from itertools import product,combinations
from random import sample
def join(a,b):
    # supremo
    return a | b

def meet(a,b):
    # infimo
    return a & b


def closure(generators):
    print("# Generated from: " + " ".join(map(str,generators)))
    news = set(generators)
    universe = set()
    rel_meet = set()
    rel_join = set()
    
    while news:
        local_news = set()
        for t in product(news,news):
            local_news.add(join(*t))
            local_news.add(meet(*t))
            rel_join.add(t+(join(*t),))
            rel_meet.add(t+(meet(*t),))
        for t in product(news,universe):
            local_news.add(join(*t))
            local_news.add(meet(*t))
            rel_join.add(t+(join(*t),))
            rel_meet.add(t+(meet(*t),))
        for t in product(universe,news):
            local_news.add(join(*t))
            local_news.add(meet(*t))
            rel_join.add(t+(join(*t),))
            rel_meet.add(t+(meet(*t),))

        local_news -= universe
        local_news -= news
        universe |= news
        news = set(local_news)
    print(" ".join(map(str,universe)))
    print("")
    print("m 2")
    for a,b,r in rel_meet:
        print("%s %s %s" % (a,b,r))
    print("")
    print("j 2")
    for a,b,r in rel_join:
        print("%s %s %s" % (a,b,r))

def main():
    generators = sample(range(1000),100)
    closure(generators)

    
if __name__ == "__main__":
    main()
