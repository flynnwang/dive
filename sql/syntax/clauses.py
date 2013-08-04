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
        return cls(prods[2])    # group by column

    def __init__(self, column):
        self.column = column

    def visit(self, ctx):
        tb = ctx.table

        def _group_by(r):
            return (r[tb.index(self.column.value)], r)
        ctx.rdd = ctx.rdd.map(_group_by)
