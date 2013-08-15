# -*- coding: utf-8 -*-

from node import Node, NodeList, ProxyNode


class SearchCondition(ProxyNode):
    pass


class BooleanValueExpr(NodeList):

    def visit(self, ctx):
        funcs = [t.visit(ctx) for t in self]

        def or_(r):
            return any(f(r) for f in funcs)
        return or_


class BooleanTerm(NodeList):

    def visit(self, ctx):
        funcs = [t.visit(ctx) for t in self]

        def and_(r):
            return all(f(r) for f in funcs)
        return and_


class BooleanFactor(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(*tokens)

    def __init__(self, not_, boolean_primary):
        self.not_ = not_
        self.boolean_primary = boolean_primary

    def visit(self, ctx):
        c = self.boolean_primary.visit(ctx)

        if self.not_:
            return lambda r: not c(r)
        return c


class BooleanPrimary(ProxyNode):
    pass


class ValueExprPrimary(ProxyNode):
    NODE_INDEX = 1


class ValueExpr(ProxyNode):
    pass
