# -*- coding: utf-8 -*-

from node import Node, TokenNode
from clauses import WhereClause, HavingClause


class SearchCondition(Node):
    """ OR logic """

    @classmethod
    def parse(cls, p):
        if len(p) == 1:
            term, more = p[0], None
        else:
            more, term = p[0], p[2]
        return SearchCondition(term, more)

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
        self.predicate, self.not_ = (p[0], False) if len(p) == 1\
            else (p[1], True)

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
