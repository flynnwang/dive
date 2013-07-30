# -*- coding: utf-8 -*-

from . import Node, IdentifierNode
from comparator import comparator


def search_condition(pg):
    @pg.production("search_condition : boolean_term")
    @pg.production("search_condition : search_condition OR boolean_term")
    def _(p):
        if len(p) == 1:
            term, more = p[0], None
        else:
            more, term = p[0], p[2]
        return SearchCondition(term, more)

    @pg.production("""boolean_term :
            row_value_designator comp_op row_value_designator""")
    def boolean_term(p):
        return BooleanTerm(*p)

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


class SearchCondition(Node):

    def __init__(self, term, more=None):
        self.term = term
        self.more = more

    def visit(self, ctx):
        c = self.term.visit(ctx)
        if self.more is None:
            return c
        
        # the OR logic
        c2 = self.more.visit(ctx)

        def _filter(r):
            return c(r) or c2(r)

        return _filter
        

class BooleanTerm(Node):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def visit(self, ctx):
        idx = ctx.table.index(self.left.value)

        def check(r):
            return self.op(r[idx], self.right.value)
        return check


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
