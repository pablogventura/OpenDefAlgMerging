# -*- coding: utf-8 -*-

#!/usr/bin/env python

"""
Modulo para calcular HIT de una tupla en un modelo
"""

from itertools import product
from collections import defaultdict
from misc import indent
from isomorphisms import Isomorphism


class TupleModelHash():
    """
    Clase de HIT, toma un modelo ambiente y la tupla generadora
    """

    def __init__(self, model, generator_tuple, th=None):
        """
        Calcula HIT de una tupla generadora en un modelo.
        Si viene en th una tupla (T,H), se considera que son
        los datos para un hit ya calculado (ie hitp)
        """
        generator_tuple = list(generator_tuple)
        self.generator_tuple = generator_tuple
        self.model = model
        self.V = list(generator_tuple)

        if th:
            # es un hit creado a partir de datos ya listos
            self.T, self.H = th
            return

        self.ops = defaultdict(set)
        for op in model.operations:
            self.ops[model.operations[op].arity].add(model.operations[op])

        self.H = [generator_tuple]
        i = len(generator_tuple)-1
        self.T = defaultdict(set, {a: {j}
                                   for j, a in enumerate(generator_tuple)})
        O = self.H[-1]

        while O:
            # esto estaba abajo de ar, entonces recalculaba el alfabeto cada vez
            flath = [item for sublist in self.H for item in sublist]
            self.H.append([])
            for ar in sorted(self.ops):
                for f in sorted(self.ops[ar], key=lambda f: f.sym):
                    for tup in product(flath, repeat=ar):
                        i += 1
                        self.V.append(str(f(*tup)))
                        if any(t in O for t in tup):
                            x = f(*tup)
                            self.T[x].add(i)
                            self.V[-1]= x
                            if all(x not in h for h in self.H):
                                self.H[-1].append(x)
            O = self.H[-1]
        self.T = {k: frozenset(self.T[k]) for k in self.T}
        self.H.pop(-1)

    def __eq__(self, other):
        return set(self.T.values()) == set(other.T.values())

    def __hash__(self):
        return hash(frozenset(self.T.values()))

    def iso(self, other):
        if self == other:
            flat_h_self = [item for sublist in self.H for item in sublist]
            flat_h_other = [item for sublist in other.H for item in sublist]
            d = {(flat_h_self[i]): flat_h_other[i]
                 for i in range(len(flat_h_self))}
            return Isomorphism(d, self.model.restrict(self.universe()),
                               other.model.restrict(other.universe()), None)
        return None

    def tuple(self):
        return self.generator_tuple

    def universe(self):
        return {item for sublist in self.H for item in sublist}

    def structure(self):
        return self.model.restrict(self.universe())

    def __repr__(self):
        result = "TupleModelHash(\n"
        result += indent("Tuple=%s,\n" % self.generator_tuple)
        result += indent("History=%s,\n" % self.H)
        result += indent("Type=%s,\n" % {k:sorted(self.T[k]) for k in self.T})
        result += indent("V=%s,\n" % self.V)
        result += ")"
        return result

    def hit_p(self, perm):
        b_i=0
        b_n=len(perm)
        sigma = list(perm)
        perm = list(perm)
        H = [list(self.tuple())]
        for Ha in self.H[1:]+[[]]:  # Saltea el primer bloque de la historia porque es la misma tulpa
                                    # y agrega al final la lista vacia porque no se crearon mas elementos

            op= list(self.ops[2])[0]
            b_i = b_n  # final del bloque anterior
            b_n += len(sigma)**op.arity
            for i in range(b_i, b_n):
                s_i = self._int2base(i-b_i, len(sigma),op.arity)
                s_i = [sigma[x] for x in s_i]
                s_i = self._base2int(s_i, len(sigma)) + b_i
                perm.append(s_i)
            H.append(sorted(Ha, key=lambda x: perm[min(self.T[x])]))
            sigma += [H[-1].index(e)+len(sigma) for e in H[-1]]
        T = dict()
        for e in self.T:
            T[e] = frozenset(perm[i] for i in self.T[e])
            d = defaultdict(lambda :" ", {perm[i]:e for i,e in enumerate(self.V)})
        V=[]
        for i in range(max(d.keys())+1):
            V.append(d[i])
            
        result = TupleModelHash(self.model, self._permute(self.generator_tuple, perm), th=(T, H)) 
        result.V=V
        return result

    def _int2base(self, number, base, size=None):
        """
        Convierte al numero x en base "base"
        como una lista de largo size de enteros.
        """
        valor = number
        assert number >= 0
        if number == 0:
            digits = [0]
        else:
            digits = []
            while number:
                digits.append(number % base)
                number = int(number / base)
            digits.reverse()
        if size:
            if size < len(digits):
                raise ValueError("%s en base %s da %s, que no entra en %s digitos" % (
                    valor, base, digits, size))
            else:
                digits = ([0] * (size-len(digits))) + digits
        return digits

    def _base2int(self, l_number, base):
        """
        Convierte una lista de numeros del 0 a base-1
        en un numero entero considerando que es una lista
        de simbolos en base "base"
        """
        result = 0
        for i, value in enumerate(reversed(l_number)):
            result += value*base**i
        return result

    def _permute(self, l, perm):
        return [l[perm[i]] for i in range(len(l))]


if __name__ == "__main__":
    """
    Para testeo
    """

    from parser import parser
    MODEL = parser("./model_examples/romboletras.model",preprocess=False)
    print(MODEL)
    TA = ["c", "d"]
    TB = ["d", "c"]
    FA = TupleModelHash(MODEL, TA)
    FB = TupleModelHash(MODEL, TB)
    FC = TupleModelHash(MODEL, TA).hit_p([1, 0])
    print(FA)
    print(FB)
    print(FC)
    print(FA == FB and FA == FC and FB == FC)
