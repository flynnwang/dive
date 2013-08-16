# -*- coding: utf-8 -*-

from node import Node, ProxyNode
from datamodel import Valueable


class Aggregatable(object):

    def create(self, v):
        return self.arg(v)

    def merge(self, v1, v2):
        return v1

    def result(self, v):
        return v

    def arg(self, r):
        return r


class Argument(ProxyNode):
    pass


class SetFunctionType(Node):

    @classmethod
    def parse(cls, tokens):
        func = tokens[0].value
        if func not in funcs:
            raise Exception("No set function found with name: %s" % func)
        return funcs[func]
        

class SetFunctionSpec(Node, Valueable):

    @classmethod
    def parse(cls, tokens):
        func = tokens[0]
        return func(tokens[2])

    @property
    def is_agg_func(self):
        return True

    def __init__(self, argument):
        self.argument = argument

    @property
    def value(self):
        return self.argument.value

    def visit(self, ctx):
        Node.visit(self, ctx)
        self.tb = ctx.table
        self.argument.visit(ctx)


class CountFunction(SetFunctionSpec, Aggregatable):

    @property
    def name(self):
        return "count"

    def create(self, r):
        v = self.argument.arg(r)
        return v is not None and 1 or 0

    def merge(self, v1, v2):
        return v1 + v2

    def result(self, v):
        return v


class SumFunction(SetFunctionSpec, Aggregatable):

    @property
    def name(self):
        return "sum"

    def create(self, r):
        v = self.argument.arg(r)
        return v

    def merge(self, v1, v2):
        return v1 + v2

    def result(self, v):
        return v


class AverageFunction(SetFunctionSpec, Aggregatable):

    @property
    def name(self):
        return "avg"

    def create(self, r):
        v = self.argument.arg(r)
        return (1, v)

    def merge(self, (c1, s1), (c2, s2)):
        return (c1 + c2, s1 + s2)

    def result(self, v):
        cnt, sum = v
        return float(sum) / cnt


funcs = {
    'count': CountFunction,
    'sum': SumFunction,
    'avg': AverageFunction,
}
