# -*- coding: utf-8 -*-
#!/usr/bin/env python

from models import RelationalModel
from relations import Relation

class ParserError(Exception):
    """
    Sintax error while parsing
    """
    def __init__(self, line, message):
        self.line = line
        self.message = message

def stdin_parser():
    """
    Returns parsed Rel_Model from stdin
    """
    linenumber = 1
    relations = {}
    try:
        universe = map(int,input().split()) # first line, universe
        linenumber += 1
        assert input() == "", ("Line #%s must be empty"%linenumber)
        linenumber += 1
        while True:
            # parsing relations
            # format:
            #   symbol number_of_tuples arity
            #   tuples
            #   empty line
            try:
                sym, ntuples, arity = input().split()
                linenumber += 1
            except EOFError:
                # no more relations found
                break

            ntuples,arity = int(ntuples),int(arity)
            relation = Relation(sym,arity)
            for i in range(ntuples):
                relation.add(tuple(map(int,input().split())))
                linenumber += 1
            assert input() == "", ("Relation must finish with empty line at #%s line"%linenumber) # relation MUST finish with empty line
            linenumber += 1
            relations[sym] = relation
    except EOFError:
        raise ParserError(linenumber,"Unexpected EOF")
    
    return RelationalModel(universe,relations)
