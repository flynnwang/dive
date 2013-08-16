# -*- coding: utf-8 -*-

from node import Node, ProxyNode


class Aggregatable(object):

    """ set_function should impl methods below """

    def create(self, r):
        return r

    def merge(self, v1, v2):
        return v1

    def result(self, v):
        return v


class Argument(ProxyNode):
    pass


class SetFunctionType(Node):

    @classmethod
    def parse(cls, tokens):
        func = tokens[0].value
        if func not in funcs:
            raise Exception("No set function found with name: %s" % func)
        return funcs[func]


class SetFunctionSpec(Node):

    func_name = 'func'

    @classmethod
    def parse(cls, tokens):
        func = tokens[0]
        return func(tokens[2])

    @property
    def is_agg_func(self):
        return True

    def __init__(self, argument):
        self.argument = argument

    def value(self, r=None):
        return self.argument.value(r)

    def visit(self, ctx):
        Node.visit(self, ctx)
        self.tb = ctx.table
        self.argument.visit(ctx)

    @property
    def name(self):
        return "%s(%s)" % (self.func_name, self.argument.name)


class CountFunction(SetFunctionSpec, Aggregatable):

    func_name = "count"

    def create(self, r):
        v = self.argument.value(r)
        return v is not None and 1 or 0

    def merge(self, v1, v2):
        return v1 + v2

    def result(self, v):
        return v


class SumFunction(SetFunctionSpec, Aggregatable):

    func_name = "sum"

    def create(self, r):
        v = self.argument.value(r)
        return v

    def merge(self, v1, v2):
        return v1 + v2

    def result(self, v):
        return v


class AverageFunction(SetFunctionSpec, Aggregatable):

    func_name = "avg"

    def create(self, r):
        v = self.argument.value(r)
        return (1, v)

    def merge(self, (c1, s1), (c2, s2)):
        return (c1 + c2, s1 + s2)

    def result(self, v):
        cnt, sum = v
        return float(sum) / cnt


class MaxFunction(SetFunctionSpec, Aggregatable):

    func_name = "max"

    def create(self, r):
        v = self.argument.value(r)
        return v

    def merge(self, v1, v2):
        return max(v1, v2)


class MinFunction(SetFunctionSpec, Aggregatable):

    func_name = "min"

    def create(self, r):
        v = self.argument.value(r)
        return v

    def merge(self, v1, v2):
        return min(v1, v2)


funcs = {
    'count': CountFunction,
    'sum': SumFunction,
    'avg': AverageFunction,
    'max': MaxFunction,
    'min': MinFunction,
}
