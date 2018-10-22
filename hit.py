# -*- coding: utf-8 -*-

#!/usr/bin/env python

"""
Modulo para calcular HIT de una tupla en un modelo
"""

from itertools import product
from collections import defaultdict
from misc import indent
from isomorphisms import Isomorphism


def int2base(number, base, size=None):
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


def base2int(l_number, base):
    """
    Convierte una lista de numeros del 0 a base-1
    en un numero entero considerando que es una lista
    de simbolos en base "base"
    """
    result = 0
    for i, value in enumerate(reversed(l_number)):
        result += value*base**i
    return result


def permute(l, perm):
    return [l[perm[i]] for i in range(len(l))]


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

        if th:
            # es un hit creado a partir de datos ya listos
            self.T, self.H = th
            return

        ops = defaultdict(set)
        for op in model.operations:
            ops[model.operations[op].arity].add(model.operations[op])

        self.H = [generator_tuple]
        i = len(generator_tuple)-1
        self.T = defaultdict(set, {a: {j}
                                   for j, a in enumerate(generator_tuple)})
        O = self.H[-1]

        while O:
            # esto estaba abajo de ar, entonces recalculaba el alfabeto cada vez
            flath = [item for sublist in self.H for item in sublist]
            self.H.append([])
            for ar in sorted(ops):
                for f in sorted(ops[ar], key=lambda f: f.sym):
                    for tup in product(flath, repeat=ar):
                        i += 1
                        if any(t in O for t in tup):
                            x = f(*tup)
                            self.T[x].add(i)
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
        result += indent("Type=%s,\n" % dict(self.T))
        result += ")"
        return result

    def hit_p(self, perm):
        sigma = list(perm)
        n = len(perm)
        H = []
        for Ha in self.H:  # Ha historia actual
            if not Ha:
                continue
            H.append(sorted(Ha, key=lambda x: perm[min(self.T[x])]))
            for op in self.model.operations:
                n += len(sigma)**self.model.operations[op].arity
                b_1 = len(perm)  # final del bloque anterior
                for i in range(b_1, n):
                    s_i = int2base(i-b_1, len(sigma),
                                   self.model.operations[op].arity)
                    s_i = [sigma[x] for x in s_i]
                    s_i = base2int(s_i, len(sigma)) + b_1
                    perm.append(s_i)
            sigma += [Ha.index(e)+len(sigma) for e in H[-1]]
        T = dict()
        for e in self.T:
            T[e] = frozenset(perm[i] for i in self.T[e])

        return TupleModelHash(self.model, permute(self.generator_tuple, perm), th=(T, H))


if __name__ == "__main__":
    from parser import parser
    MODEL = parser("./malvada.model")
    TA = [2, 3]
    TB = [3, 2]
    FA = TupleModelHash(MODEL, TA)
    FB = TupleModelHash(MODEL, TB)  # .hit_p([1,0])
    print(FA)
    print(FB)
    print(FA == FB)
