# -*- coding: utf-8 -*-

from node import Node, NodeList
from functools import total_ordering
from itertools import izip


class Clause(Node):
    pass


class EmptyClause(Clause):

    @classmethod
    def parse(cls, prods):
        return cls()


class EmptyGroupbyClause(EmptyClause):

    def visit(self, ctx):
        ctx.rdd = ctx.rdd.map(lambda r: (None, r))


class WhereClause(Clause):

    @classmethod
    def parse(cls, prods):
        if len(prods) == 0:
            return None
        return cls(prods[1])

    def __init__(self, search_condition):
        self.search_condition = search_condition

    def visit(self, ctx):
        _filter = self.search_condition.visit(ctx)
        ctx.rdd = ctx.rdd.filter(_filter)


class GroupByClause(Clause):

    @classmethod
    def parse(cls, prods):
        if isinstance(prods[0], EmptyClause):
            return prods[0]
        return cls(prods[2])    # group by columns

    def __init__(self, columns):
        self.columns = columns

    def visit(self, ctx):
        tb = ctx.table

        def _group_by(r):
            grouping = [r[tb.index(c.value)] for c in self.columns]
            return (tuple(grouping), r)
        ctx.rdd = ctx.rdd.map(_group_by)


class GroupingColumnList(NodeList):
    pass


class HavingClause(WhereClause):
    pass


class OrderByClause(Clause):

    @classmethod
    def parse(cls, tokens):
        if isinstance(tokens[0], EmptyOrderByClause):
            return tokens[0]
        return cls(tokens[2])    # orderby by columns ordering

    def __init__(self, sort_spec):
        self.sort_spec = sort_spec

    def visit(self, ctx):
        tb = ctx.result_table
        sort_spec = self.sort_spec

        @total_ordering
        class Ordered(object):

            def __init__(self, r):
                self.r = r

            def __le__(self, other):
                for u, v, spec in izip(self.keys, other.keys, sort_spec):
                    result = cmp(u, v)
                    if result == 0:
                        continue
                    if spec.desc:
                        result = -result
                    return result < 0
                return True

            @property
            def keys(self):
                return (self.r[tb.index(spec.column.value)]
                        for spec in sort_spec)

        ctx.rdd = ctx.rdd.map(lambda r: Ordered(r))\
                     .sort().map(lambda o: o.r)


class EmptyOrderByClause(EmptyClause):

    def visit(self, ctx):
        ctx.rdd = ctx.rdd.sort()


class SortSpecList(GroupingColumnList):
    pass


class OrderingSpec(Node):

    @classmethod
    def parse(cls, tokens):
        if len(tokens) == 2 and tokens[1].value == 'desc':
            return cls(tokens[0], desc=True)
        return cls(tokens[0])

    def __init__(self, column, desc=False):
        self.column = column
        self.desc = desc


class LimitClause(Clause):

    @classmethod
    def parse(cls, tokens):
        if len(tokens) == 2:
            return cls(int(tokens[1].value))

    def __init__(self, limit):
        self.value = limit

    def visit(self, ctx):
        ctx.rdd = ctx.rdd.take(self.limit)
