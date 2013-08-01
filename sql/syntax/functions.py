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


class CountFunction(AttributeFunction):

    def __call__(self, ctx):
        tb = ctx.table
        return ctx.rdd.map(lambda r: r[tb.index(self.column.value)]).count()
 

funcs = {
    'count': CountFunction,
}


