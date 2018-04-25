# -*- coding: utf-8 -*-
#!/usr/bin/env python

from itertools import combinations
from functools import lru_cache

from nuevosub import tipoSub

class Model(object):
    def __init__(self, universe, relations, operations):
        """
        Model
        Input: a universe list, relations dict, operations dict
        """
        self.universe = list(universe)
        self.relations = relations
        self.operations = operations


    def __repr__(self):
        return ("Model(universe=%s,relations=%s,operations=%s)" % (self.universe, self.relations, self.operations))

    def __len__(self):
        return len(self.universe)

    def spectrum(self, subtype):
        result = set()
        return result.union(*[self.relations[r].spectrum() for r in subtype])
