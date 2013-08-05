# -*- coding: utf-8 -*-

from node import Node


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
