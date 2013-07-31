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

    @pg.production("boolean_term : boolean_factor")
    @pg.production("boolean_term : boolean_term AND boolean_factor")
    def boolean_term(p):
        return BooleanTerm(p)

    @pg.production("boolean_factor : boolean_primary")
    @pg.production("boolean_factor : NOT boolean_primary")
    def boolean_factor(p):
        return BooleanFactor(p)

    @pg.production("""boolean_primary :
            row_value_designator comp_op row_value_designator""")
    def boolean_primary(p):
        return BooleanPrimary(*p)

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
    """ OR logic """

    def __init__(self, term, more=None):
        self.term = term
        self.more = more

    def visit(self, ctx):
        c = self.term.visit(ctx)
        if self.more is None:
            return c
        c2 = self.more.visit(ctx)
        return lambda r: c(r) or c2(r)


class BooleanTerm(Node):
    """ AND logic """

    def __init__(self, p):
        self.factor, self.more = (p[0], None) if len(p) == 1 else (p[2], p[0])

    def visit(self, ctx):
        c = self.factor.visit(ctx)
        if self.more is None:
            return c
        c2 = self.more.visit(ctx)
        return lambda r: c(r) and c2(r)
        

class BooleanPrimary(Node):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def visit(self, ctx):
        idx = ctx.table.index(self.left.value)

        def check(r):
            return self.op(r[idx], self.right.value)
        return check


class BooleanFactor(object):

    def __init__(self, p):
        self.predicate, self.not_ = (p[0], False) if len(p) == 1\
            else (p[1], True)

    def visit(self, ctx):
        c = self.predicate.visit(ctx)
        if self.not_:
            return lambda r: not c(r)
        return c


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
