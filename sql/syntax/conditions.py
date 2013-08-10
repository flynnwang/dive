# -*- coding: utf-8 -*-

from node import Node, TokenNode, NodeList
from clauses import WhereClause, HavingClause


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
        return lambda r: any(f(r) for f in funcs)


class BooleanTerm(NodeList):

    """ AND """

    @property
    def factors(self):
        return [self[0]] + self[1]

    def visit(self, ctx):
        funcs = filter(None, [t.visit(ctx) for t in self.factors])
        return lambda r: all(f(r) for f in funcs)


class BooleanFactor(Node):

    """ NOT """

    def __init__(self, nodes):
        self.not_, self.boolean_primary = nodes

    @property
    def predicate(self):
        return self.boolean_primary.predicate.predicate

    def visit(self, ctx):
        c = self.predicate.visit(ctx)
        if self.not_:
            return lambda r: not c(r)
        return c


class BooleanPrimary(Node):

    def __init__(self, tokens):
        self.predicate = tokens[0]


class Predicate(Node):

    def __init__(self, nodes):
        Node.__init__(self)
        self.predicate = nodes[0]
        
    def _get_table_by_clause(self, ctx):
        node = self
        while True:
            node = node.parent
            if isinstance(node, HavingClause):
                return ctx.result_table
            elif isinstance(node, WhereClause):
                return ctx.table


class InPredicate(Predicate):

    def __init__(self, tokens):
        Node.__init__(self)
        self.row_designator, self.not_, _, self.predicate_value = tokens

    def visit(self, ctx):
        tb = self._get_table_by_clause(ctx)
        idx = tb.index(self.row_designator.value)

        def in_(r):
            v = r[idx] in self.predicate_value.value
            return not v if self.not_ else v
        return in_


class InPredicateValue(Node):

    def __init__(self, nodes):
        self.value_list = nodes[1]

    @property
    def value(self):
        return self.value_list.value


class InValueList(NodeList):

    @property
    def value(self):
        return [self[0].value] + [v.value for v in self[1]]
        

class ComparisonPredicate(Predicate):

    def __init__(self, nodes):
        self.left, self.op, self.right = nodes

    def visit(self, ctx):
        tb = self._get_table_by_clause(ctx)
        idx = tb.index(self.left.value)

        def check(r):
            return self.op(r[idx], self.right.value)
        return check


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


class RowValueDesignator(Node):

    def __init__(self, tokens):
        self.value_expr = tokens[0]

    @property
    def value(self):
        return self.value_expr.value


class ValueExpr(TokenNode):

    @classmethod
    def parse(cls, tokens):
        tk = tokens[0]
        return tk.name in DESIGNATORS and DESIGNATORS[tk.name](tk) or cls(tk)


DESIGNATORS = {
    'STRING': String,
    'NUMBER': Number,
}
