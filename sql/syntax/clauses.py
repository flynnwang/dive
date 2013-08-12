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
        return cls(prods[1])

    def __init__(self, search_condition):
        self.search_condition = search_condition

    def visit(self, ctx):
        _filter = self.search_condition.boolean_value_expr.visit(ctx)
        ctx.rdd = ctx.rdd.filter(_filter)


class HavingClause(WhereClause):
    pass


class GroupByClause(Clause):

    @classmethod
    def parse(cls, prods):
        return cls(prods[2].flattened_nodes)

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


class OrderByClause(Clause):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[2])

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
                comp = [cmp(u, v) * spec.ordering for u, v, spec in
                        izip(self.keys, other.keys, sort_spec.flattened_nodes)]
                return comp <= [0] * len(comp)

            @property
            def keys(self):
                return (self.r[tb.index(spec.column.value)]
                        for spec in sort_spec.flattened_nodes)

        ctx.rdd = ctx.rdd.map(lambda r: Ordered(r))\
                     .sort().map(lambda o: o.r)


class EmptyOrderByClause(EmptyClause):

    def visit(self, ctx):
        ctx.rdd = ctx.rdd.sort()


class SortSpecList(NodeList):
    pass


class OrderingSpec(Node):

    @classmethod
    def parse(cls, tokens):
        ordering = tokens[1].value == 'desc' and -1 or 1
        return cls(tokens[0], ordering)

    def __init__(self, column, ordering):
        self.column = column
        self.ordering = ordering


class LimitClause(Clause):

    @classmethod
    def parse(cls, tokens):
        # TODO remove if
        if len(tokens) == 2:
            return cls(int(tokens[1].value))

    def __init__(self, limit):
        self.value = limit


class OutfileClause(Clause):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[2].value)

    def __init__(self, filedir):
        self.filedir = filedir
