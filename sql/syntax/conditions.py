# -*- coding: utf-8 -*-

import re
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

    def visit(self, ctx):
        return self.predicate.visit(ctx)


class LikePredicate(Predicate):

    def __init__(self, tokens):
        Node.__init__(self)
        self.row_designator, self.not_, _, self.pattern = tokens
        self.re = re.compile(self.pattern.value[1:-1])

    def visit(self, ctx):
        tb = self._get_table_by_clause(ctx)
        idx = tb.index(self.row_designator.value)

        def like_(r):
            v = self.re.match(r[idx])
            return not v if self.not_ else v
        return like_


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
       

class ValueExprPrimary(Node):

    def __init__(self, tokens):
        self.boolean_value_expr = tokens[1]

    def visit(self, ctx):
        return self.boolean_value_expr.visit(ctx)


class ValueExpr(TokenNode):

    @classmethod
    def parse(cls, tokens):
        tk = tokens[0]
        return tk.name in DESIGNATORS and DESIGNATORS[tk.name](tk) or cls(tk)


DESIGNATORS = {
    'STRING': String,
    'NUMBER': Number,
}
