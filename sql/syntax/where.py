# -*- coding: utf-8 -*-

from node import Node


class Clause(Node):
    pass


class EmptyClause(Clause):
    pass


class WhereClause(Clause):

    @classmethod
    def parse(cls, prods):
        if isinstance(prods[0], EmptyClause):
            return prods[0]
        return cls(prods, prods[1])

    def __init__(self, p, search_condition):
        Node.__init__(self, p)
        self.search_condition = search_condition

    def visit(self, ctx):
        _filter = self.search_condition.visit(ctx)
        ctx.rdd = ctx.rdd.filter(_filter)
