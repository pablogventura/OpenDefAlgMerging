# -*- coding: utf-8 -*-
#!/usr/bin/env python

from models import Model
from relops import Relation, Operation


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
    operations = {}
    try:
        universe = [int(i) for i in input().split()]  # first line, universe
        linenumber += 1
        assert input() == "", ("Line #%s must be empty" % linenumber)
        linenumber += 1
        while True:
            # parsing operations and relations
            # operations format:
            #   symbol arity
            #   (arity+1)-uples
            #   empty line
            # relations format:
            #   symbol number_of_tuples arity
            #   tuples
            #   empty line
            try:
                ro_line = input().split()
                linenumber += 1
            except EOFError:
                # no more relations found
                break
            if len(ro_line) == 3:
                # parsing relation
                sym, ntuples, arity = ro_line
                ntuples, arity = int(ntuples), int(arity)
                relation = Relation(sym, arity)
                for i in range(ntuples):
                    relation.add(tuple(map(int, input().split())))
                    linenumber += 1
                assert input() == "", ("Rel/Op must finish with empty line at #%s line" %
                                       linenumber)  # relation MUST finish with empty line
                linenumber += 1
                relations[sym] = relation
            elif len(ro_line) == 2:
                # parsing operation
                sym, arity = ro_line
                arity = int(arity)
                operation = Operation(sym, arity)
                ntuples = len(universe)**arity
                for i in range(ntuples):
                    operation.add(tuple(map(int, input().split())))
                    linenumber += 1
                assert input() == "", ("Rel/Op must finish with empty line at #%s line" %
                                       linenumber)  # relation MUST finish with empty line
                linenumber += 1
                operations[sym] = operation
            else:
                raise ParserError(linenumber, "Unexpected line")
    except EOFError:
        raise ParserError(linenumber, "Unexpected EOF")

    return Model(universe, relations, operations)
