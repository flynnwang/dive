# -*- coding: utf-8 -*-

from node import Node
from functools import total_ordering


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
        if isinstance(prods[0], EmptyClause):
            return prods[0]
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


class GroupingColumnList(Node, list):

    @classmethod
    def parse(cls, p):
        if len(p) == 1:
            columns = GroupingColumnList()
            c = p[0]
        else:
            columns, c = p[0], p[2]
        columns.append(c)
        return columns


class HavingClause(WhereClause):
    pass


class OrderByClause(Clause):

    @classmethod
    def parse(cls, tokens):
        if isinstance(tokens[0], EmptyOrderByClause):
            return tokens[0]
        return cls(tokens[2], tokens[3])    # orderby by columns ordering

    def __init__(self, columns, orderby):
        self.columns = columns
        self.orderby = orderby

    def visit(self, ctx):
        tb = ctx.result_table
        columns = self.columns
        orderby = self.orderby

        @total_ordering
        class Ordered(object):

            def __init__(self, r):
                self.r = r

            def __lt__(self, other):
                result = self.key < other.key
                if orderby.desc:
                    result = not result
                return result

            @property
            def key(self):
                return [self.r[tb.index(c.value)] for c in columns]

        ctx.rdd = ctx.rdd.map(lambda r: Ordered(r))\
                     .sort().map(lambda o: o.r)


class EmptyOrderByClause(EmptyClause):

    def visit(self, ctx):
        ctx.rdd = ctx.rdd.sort()


class SortSepcList(GroupingColumnList):
    pass


class OrderingSpec(Node):

    @classmethod
    def parse(cls, tokens):
        if len(tokens) == 1 and tokens[0].value == 'desc':
            return cls(desc=True)
        return cls(desc=False)

    def __init__(self, desc=False):
        self.desc = desc
