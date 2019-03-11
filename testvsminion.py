from parser import parser
from random import sample
import sys
from hit import TupleModelHash
from time import time


def main():
    model = parser(sys.argv[1])
    
    ta = [0,1,2]
    tb = sample(model.universe,3)
    
    start_hit = time()
    TupleModelHash(model,ta) == TupleModelHash(model,tb)
    time_hit = time() - start_hit
    
    
    start_minion = time()
    a=model.substructure(ta)
    print(a)
    #b=model.substructure(tb)
    #print (b)
    ra=a.to_relational_model()
    #rb=b.to_relational_model()
    print(ra)
    time_minion = time() - start_minion
    
        
if __name__ == "__main__":
    main()
