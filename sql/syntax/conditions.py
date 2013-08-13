# -*- coding: utf-8 -*-

from node import Node, NodeList, WrapNode


class SearchCondition(Node):

    def __init__(self, tokens):
        self.boolean_value_expr = tokens[0]


class BooleanValueExpr(NodeList):

    """ OR """

    @property
    def terms(self):
        return [self[0]] + self[1]

    def visit(self, ctx):
        funcs = filter(None, [t.visit(ctx) for t in self.terms])

        def or_(r):
            return any(f(r) for f in funcs)
        return or_


class BooleanTerm(NodeList):

    """ AND """

    @property
    def factors(self):
        return [self[0]] + self[1]

    def visit(self, ctx):
        funcs = filter(None, [t.visit(ctx) for t in self.factors])

        def and_(r):
            return all(f(r) for f in funcs)
        return and_


class BooleanFactor(Node):

    """ NOT """

    def __init__(self, nodes):
        self.not_, self.boolean_primary = nodes

    def visit(self, ctx):
        c = self.boolean_primary.visit(ctx)
        if self.not_:
            return lambda r: not c(r)
        return c


class BooleanPrimary(Node):

    def __init__(self, tokens):
        self.node = tokens[0]

    def visit(self, ctx):
        return self.node.visit(ctx)


class RowValueDesignator(Node):

    def __init__(self, tokens):
        self.value_expr = tokens[0]

    @property
    def value(self):
        return self.value_expr.value
       

class ValueExprPrimary(Node):

    def __init__(self, tokens):
        self.boolean_value_expr = tokens[1]

    def visit(self, ctx):
        return self.boolean_value_expr.visit(ctx)


class ValueExpr(WrapNode):

    @classmethod
    def parse(cls, tokens):
        return tokens[0]
