from parser import parser
from random import sample
import sys
from hit import TupleModelHash
from time import time
from minion import is_isomorphic

def main():
    model = parser(sys.argv[1])
    
    
    ta = sample(model.universe,3)
    tb = tuple(ta)#sample(model.universe,3)
    
    start_hit = time()
    hit_return = TupleModelHash(model,ta) == TupleModelHash(model,tb)
    time_hit = time() - start_hit
    
    
    start_minion = time()
    a=model.substructure(ta)
    b=model.substructure(tb)
    subtype = sorted(model.relations.keys())
    ra=a.to_relational_model()
    rb=b.to_relational_model()
    minion_return = is_isomorphic(ra,rb,subtype) != False
    time_minion = time() - start_minion
    print("*"*80)
    print("Hit(%s) == Hit(%s) = %s, time= %s" % (ta,tb,hit_return,time_hit))
    print("Minion(%s) == Minion(%s) = %s, time= %s" % (ta,tb,minion_return,time_minion))
    
        
if __name__ == "__main__":
    main()
