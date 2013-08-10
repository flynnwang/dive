# -*- coding: utf-8 -*-

import re
import operator as op
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
        return op.eq(x, y)


class LessThan(Comparator):

    def __call__(self, x, y):
        return op.lt(x, y)


class LessThanOrEqual(Comparator):

    def __call__(self, x, y):
        return op.le(x, y)


class GreaterThan(Comparator):

    def __call__(self, x, y):
        return op.gt(x, y)


class GreaterThanOrEqual(Comparator):

    def __call__(self, x, y):
        return op.ge(x, y)


class LikeComparator(Comparator):

    def __call__(self, x, y):
        # TODO pre compile re
        return re.match(y, x)

COMPARATORS = {
    '=': Equal,
    '<': LessThan,
    '<=': LessThanOrEqual,
    '>': GreaterThan,
    '>=': GreaterThanOrEqual,
    'like': LikeComparator,
}
