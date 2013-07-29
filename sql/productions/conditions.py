# -*- coding: utf-8 -*-

from . import Node, IdentifierNode
from comparator import comparator


def search_condition(pg):
    @pg.production("search_condition : ")
    @pg.production("search_condition : boolean_expr")
    def _(p):
        return p[0]

    @pg.production("""boolean_expr :
            row_value_designator comp_op row_value_designator""")
    def boolean_expr(p):
        return BooleanExpr(*p)

    @pg.production("row_value_designator : IDENTIFIER")
    def row_value_designator(p):
        return RowValueDesignator(p[0])

    @pg.production("row_value_designator : NUMBER")
    def row_value_designator_as_number(p):
        return Number(p[0])

    @pg.production("row_value_designator : STRING")
    def row_value_designator_as_string(p):
        return String(p[0])

    comparator(pg)

    return pg


class Predicate(Node):
    pass


class BooleanExpr(Predicate):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def visit(self, ctx):
        idx = ctx.table.index(self.left.value)

        def check(r):
            return self.op(r[idx], self.right.value)

        ctx.rdd = ctx.rdd.filter(check)


class Number(Node):

    def __init__(self, token):
        self.token = token
        self.value = int(token.value)


class String(Node):
    # TODO: create a token node type

    def __init__(self, token):
        self.token = token
        self.value = token.value[1:-1]


class RowValueDesignator(IdentifierNode):
    pass
