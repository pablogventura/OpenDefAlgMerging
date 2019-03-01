import networkx
import random
import itertools
def generate_cover_relation(nodes,edges,gamma=3):
    assert edges < nodes, "Not possible"
    while True:
        try:
            g = networkx.random_powerlaw_tree(nodes, gamma=3, seed=None, tries=100)
            if len(g.edges()) >= edges:
                return random.sample(g.edges(),edges)
        except networkx.NetworkXError:
            continue


def ascendants(nodes, cover):
    ascendants = {n:{n} for n in range(nodes)}
    
    for e in range(nodes):
        for ee,b in cover:
            if e==ee:
                ascendants[e].add(b)
    
    universe = {frozenset(),frozenset(range(nodes))}
    for n in ascendants:
        universe.add(frozenset(ascendants[n]))
    
    return universe
    
def random_lattice(nodes, edges, gamma=3):
    return ascendants(nodes,generate_cover_relation(nodes,edges,gamma))

