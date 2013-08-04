# -*- coding: utf-8 -*-

from node import Node


class AttributeFunction(Node):

    def __init__(self, token, column):
        self._token = token
        self.column = column

    @classmethod
    def parse(cls, prods):
        func = prods[0].value
        if func not in funcs:
            raise Exception("No attibute function found: %s" % func)
        return funcs[func](prods[0], prods[2])

    @property
    def value(self):
        return self._token.value


class AggregateFunction(AttributeFunction):

    def create(self, v):
        return v

    def merge(self, v1, v2):
        return v1

    def result(self, v):
        return v


class CountFunction(AggregateFunction):

    def create(self, v):
        return v is not None and 1 or 0

    def merge(self, v1, v2):
        return v1 + v2

    def result(self, v):
        return v


class SumFunction(AggregateFunction):

    def create(self, v):
        return v

    def merge(self, v1, v2):
        return v1 + v2

    def result(self, v):
        return v


class AverageFunction(AggregateFunction):

    def create(self, v):
        return (1, v)

    def merge(self, (c1, s1), (c2, s2)):
        return (c1+c2, s1+s2)

    def result(self, v):
        cnt, sum = v
        return float(sum) / cnt


funcs = {
    'count': CountFunction,
    'sum': SumFunction,
    'avg': AverageFunction,
}


