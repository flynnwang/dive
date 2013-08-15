# -*- coding: utf-8 -*-

from node import Node
from datamodel import Valueable


class Aggregatable(object):

    def create(self, v):
        return v

    def merge(self, v1, v2):
        return v1

    def result(self, v):
        return v

    def arg(self, r):
        return r


class AttributeFunction(Node, Valueable):

    @property
    def is_agg_func(self):
        return True

    def __init__(self, token, column):
        self._token = token
        self.column = column

    @classmethod
    def parse(cls, tokens):
        func = tokens[0].value
        if func not in funcs:
            raise Exception("No attibute function found: %s" % func)
        return funcs[func](tokens[0], tokens[2])

    @property
    def value(self):
        return self.column.value

    @property
    def name(self):
        return self._token.value

    def visit(self, ctx):
        self.tb = ctx.table
        self.column.visit(ctx)


class CountFunction(AttributeFunction, Aggregatable):

    def create(self, r):
        v = self.column.create(r)
        return v is not None and 1 or 0

    def merge(self, v1, v2):
        return v1 + v2

    def result(self, v):
        return v


class SumFunction(AttributeFunction, Aggregatable):

    def create(self, v):
        return v

    def merge(self, v1, v2):
        return v1 + v2

    def result(self, v):
        return v


class AverageFunction(AttributeFunction, Aggregatable):

    def create(self, v):
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
