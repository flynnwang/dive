# -*- coding: utf-8 -*-

from . import Node
import conditions


def where_clause(pg):
    @pg.production("where_clause : WHERE search_condition")
    @pg.production("where_clause : empty")
    def where_clause(p):
        return p[0] is not None and WhereClause(p[1])

    conditions.search_condition(pg)


class Clause(Node):
    pass


class WhereClause(Clause):

    def __init__(self, search_condition):
        self.search_condition = search_condition

    def visit(self, ctx):
        self.search_condition.visit(ctx)
