# -*- coding: utf-8 -*-
#!/usr/bin/env python


class CounterexampleTuples(Exception):
    def __init__(self, a,b):
        super(CounterexampleTuples, self).__init__("Orbits %s and %s have the same type, but polarities differ" % (a,b))
