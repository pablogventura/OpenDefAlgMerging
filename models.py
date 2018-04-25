# -*- coding: utf-8 -*-
#!/usr/bin/env python


from itertools import combinations
from functools import lru_cache
from nuevosub import tipoSub

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
        self.universe = list(universe)
        self.relations = relations
        self.operations = operations

    def substructure(self, subuniverse):
        relations = {}
        operations = {}
        for r in self.relations:
            relations[r] = self.relations[r].restrict(subuniverse)
        for f in self.operations:
            operations[f] = self.operations[f].restrict(subuniverse)
        yield Model(subuniverse, relations, operations)

    def __repr__(self):
        return ("Model(universe=%s,relations=%s,operations=%s)" % (self.universe, self.relations, self.operations))

    @lru_cache(maxsize=2)
    def rels_sizes(self, subtype):
        return PartialOrderedDict({r: len(self.relations[r]) for r in subtype})

    @lru_cache(maxsize=None)
    def minion_tables(self, subtype):
        result = ""
        for r in subtype:
            result += "%s %s %s\n" % (r,
                                      len(self.relations[r]), self.relations[r].arity)
            for t in self.relations[r]:
                result += " ".join(str(self.universe.index(x))
                                   for x in t) + "\n"
            result += "\n"
        return result[:-1]

    def minion_constraints(self, subtype):
        result = ""
        # table([f[0],f[0],f[0]],bv)
        result = ""
        for r in subtype:
            for t in self.relations[r]:
                result += "table([f["
                result += "],f[".join(str(self.universe.index(x)) for x in t)
                result += "]],%s)\n" % r
        return result

    def __len__(self):
        return len(self.universe)

    def spectrum(self, subtype):
        result = set()
        return result.union(*[self.relations[r].spectrum() for r in subtype])
