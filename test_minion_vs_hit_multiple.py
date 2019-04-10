from parser.parser import parser
from random import sample,seed
import sys
from hit import TupleModelHash
from time import time
from interfaces.minion import is_isomorphic
from colorama import Fore, Style
from itertools import product
seed(1)

def main():
    model = parser(sys.argv[1], verbose=False)
    model.relations = {} # este test es sin relaciones
    
    tuples=[]
    for i in range(8):
        tuples.append(tuple(sample(model.universe, 3)))
    # estan generadas las tuplas
        
    start_hit = time()
    hits = []
    for t in tuples:
        hits.append(TupleModelHash(model, t))
    return_hits=[]
    for h1,h2 in product(hits,hits):
        return_hits.append(h1==h2)
    time_hit = time() - start_hit
        
    start_minion = time()
    substructures = dict()
    for t in tuples:
        substructures[t] = model.substructure(t).to_relational_model()
    subtype = sorted(substructures[tuples[0]].relations.keys())
    # print("Subtipo %s" % subtype)
    return_minion=[]
    for t1, t2 in product(substructures.keys(), substructures.keys()):
        return_minion.append(bool(is_isomorphic(substructures[t1], substructures[t2], subtype, t1, t2)))
    time_minion = time() - start_minion
    return_hits= "".join(str(int(i)) for i in return_hits)
    return_minion = "".join(str(int(i)) for i in return_minion)
    # print(return_hits.count("1"))
    # print(return_minion.count("1"))
    # assert return_minion==return_hits
    # return_hits = int(return_hits, 2)
    # return_minion = int(return_minion, 2)
    # return_hits = hash(return_hits)
    # return_minion = hash(return_minion)
    
    print("*" * 80)
    if time_hit <= time_minion:
        print(Fore.GREEN + "Hit    = %s, hit/minion= %s" % (return_hits, time_hit / time_minion) + Style.RESET_ALL)
        print(Fore.RED + "Minion = %s, minion/hit= %s" % (return_minion, time_minion / time_hit) + Style.RESET_ALL)
    else:
        print(Fore.RED + "Hit = %s, hit/minion= %s" % (return_hits, time_hit / time_minion) + Style.RESET_ALL)
        print(Fore.GREEN + "Minion = %s, minion/hit= %s" % (return_minion, time_minion / time_hit) + Style.RESET_ALL)
    

if __name__ == "__main__":
    j=main()