# -*- coding: utf-8 -*-

import re
from node import Node, NodeList
from clauses import WhereClause, HavingClause


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
        self.column, self.not_, _, self.pattern = tokens
        self.re = re.compile(self.pattern.value)

    def visit(self, ctx):
        tb = self._get_table_by_clause(ctx)
        idx = tb.index(self.column.value)

        def like_(r):
            v = self.re.match(r[idx])
            return not v if self.not_ else v
        return like_


class InPredicate(Predicate):

    def __init__(self, tokens):
        Node.__init__(self)
        self.column, self.not_, _, self.predicate_value = tokens

    def visit(self, ctx):
        tb = self._get_table_by_clause(ctx)
        idx = tb.index(self.column.value)

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
