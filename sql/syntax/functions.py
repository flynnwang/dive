# -*- coding: utf-8 -*-

from node import TokenNode


class AttributeFunction(TokenNode):

    def __init__(self, prods, token, column):
        TokenNode.__init__(self, prods, token)
        self._token = token
        self.column = column

    @classmethod
    def parse(cls, prods):
        func = prods[0].value
        if func not in funcs:
            raise Exception("No attibute function found: %s" % func)
        return funcs[func](prods, prods[0], prods[2])


class AggregateFunction(AttributeFunction):

    def create(self, v):
        raise Exception("No implememtation exception")

    def merge(self, v1, v2):
        raise Exception("No implememtation exception")

    #def result(self, v):
        #raise Exception("No implememtation exception")


class CountFunction(AggregateFunction):

    def create(self, v):
        return v is not None and 1 or 0

    def merge(self, v1, v2):
        return v1 + v2


funcs = {
    'count': CountFunction,
}


