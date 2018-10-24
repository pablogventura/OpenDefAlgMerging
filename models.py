# -*- coding: utf-8 -*-
#!/usr/bin/env python

from itertools import combinations
from functools import lru_cache


class PartialOrderedDict(dict):
    def __lt__(self, other):  # <
        return self <= other and self != other

    def __gt__(self, other):  # >
        return self >= other and self != other

    def __le__(self, other):  # <=
        for k in self:
            if not self[k] <= other[k]:
                return False
        return True

    def __ge__(self, other):  # >=
        for k in self:
            if not self[k] >= other[k]:
                return False
        return True


class Model(object):
    def __init__(self, universe, relations, operations):
        """
        Model
        Input: a universe list, relations dict, operations dict
        """
        self.universe = set(universe)
        self.relations = relations
        self.operations = operations

    def restrict(self, subuniverse):
        """
        restricion de un subuniverso a ciertas relaciones
        """
        relations = {}
        for r in self.relations:
            relations[r] = self.relations[r].restrict(subuniverse)
        operations = {}
        for o in self.operations:
            operations[o] = self.operations[o].restrict(subuniverse)
        return Model(subuniverse, relations, operations)

    @lru_cache(maxsize=None)
    def rels_sizes(self, subtype):
        return PartialOrderedDict({r: len(self.relations[r]) for r in subtype})

    def __repr__(self):
        return ("Model(universe=%s,relations=%s,operations=%s)" % (self.universe, self.relations, self.operations))

    def __len__(self):
        return len(self.universe)

    def spectrum(self, subtype):
        result = set()
        return result.union(*[self.relations[r].spectrum() for r in subtype])
