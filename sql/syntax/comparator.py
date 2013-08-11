# -*- coding: utf-8 -*-

import operator
from node import TokenNode


class Comparator(TokenNode):

    @classmethod
    def parse(cls, tokens):
        tk = tokens[0]
        return COMPARATORS[tk.value](tk)

    def __call__(self, x, y):
        raise Exception("NOT IMPLEMENTED")


class Equal(Comparator):

    def __call__(self, x, y):
        return operator.eq(x, y)


class LessThan(Comparator):

    def __call__(self, x, y):
        return operator.lt(x, y)


class LessThanOrEqual(Comparator):

    def __call__(self, x, y):
        return operator.le(x, y)


class GreaterThan(Comparator):

    def __call__(self, x, y):
        return operator.gt(x, y)


class GreaterThanOrEqual(Comparator):

    def __call__(self, x, y):
        return operator.ge(x, y)

COMPARATORS = {
    '=': Equal,
    '<': LessThan,
    '<=': LessThanOrEqual,
    '>': GreaterThan,
    '>=': GreaterThanOrEqual,
}
