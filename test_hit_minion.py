

from parser import parser
from hit import TupleModelHash

model = parser(sys.argv[1])

t = [0,1,2]

TupleModelHash(t) == TupleModelHash(t)

minion_model = model.substructure(t)
