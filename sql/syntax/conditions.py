# -*- coding: utf-8 -*-

from node import Node, TokenNode, NodeList
from clauses import WhereClause, HavingClause


class SearchCondition(NodeList):
    """ OR logic """

    @property
    def terms(self):
        return [self[0]] + self[1]

    def visit(self, ctx):
        funcs = filter(None, [t.visit(ctx) for t in self.terms])
        return lambda r: any(f(r) for f in funcs)


class BooleanTerm(NodeList):
    """ AND logic """

    @property
    def factors(self):
        return [self[0]] + self[1]

    def visit(self, ctx):
        funcs = filter(None, [t.visit(ctx) for t in self.factors])
        return lambda r: all(f(r) for f in funcs)
        

class BooleanPrimary(Node):

    @classmethod
    def parse(cls, prods):
        return cls(*prods)

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def _get_table_by_clause(self, ctx):
        node = self
        while True:
            node = node.parent
            if isinstance(node, HavingClause):
                return ctx.result_table
            elif isinstance(node, WhereClause):
                return ctx.table

    def visit(self, ctx):
        tb = self._get_table_by_clause(ctx)
        idx = tb.index(self.left.value)

        def check(r):
            return self.op(r[idx], self.right.value)
        return check


class BooleanFactor(Node):
    """ NOT """

    def __init__(self, p):
        self.not_, self.predicate = p

    def visit(self, ctx):
        c = self.predicate.visit(ctx)
        if self.not_:
            return lambda r: not c(r)
        return c


class Number(TokenNode):

    def __init__(self, token):
        TokenNode.__init__(self, token)
        self._val = int(token.value)

    @property
    def value(self):
        return self._val


class String(TokenNode):

    def __init__(self, token):
        TokenNode.__init__(self, token)
        self._val = token.value[1:-1]

    @property
    def value(self):
        return self._val


class RowValueDesignator(TokenNode):

    @classmethod
    def parse(cls, tokens):
        tk = tokens[0]
        return tk.name in DESIGNATORS and DESIGNATORS[tk.name](tk) or cls(tk)


DESIGNATORS = {
    'STRING': String,
    'NUMBER': Number,
}
