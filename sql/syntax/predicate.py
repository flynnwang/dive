# -*- coding: utf-8 -*-

import re
from node import Node, NodeList, ProxyNode
from clauses import WhereClause, HavingClause


class Predicate(ProxyNode):

    def _get_table_by_clause(self, ctx):
        node = self
        while True:
            # pylint: disable=E1101
            node = node.parent
            if isinstance(node, HavingClause):
                return ctx.result_table
            elif isinstance(node, WhereClause):
                return ctx.table


class LikePredicate(Predicate):

    @classmethod
    def parse(cls, tokens):
        return cls(column=tokens[0], not_=tokens[1], pattern=tokens[3])

    def __init__(self, column, not_, pattern):
        Node.__init__(self)
        self.column = column
        self.not_ = not_
        self.pattern = re.compile(pattern.value())

    def visit(self, ctx):
        tb = self._get_table_by_clause(ctx)
        idx = tb.index(self.column.value())

        def like_(r):
            v = self.pattern.match(r[idx])
            return not v if self.not_ else v
        return like_


class InPredicate(Predicate):

    @classmethod
    def parse(cls, tokens):
        return cls(column=tokens[0], not_=tokens[1], predicate_value=tokens[3])

    def __init__(self, column, not_, predicate_value):
        Node.__init__(self)
        self.column = column
        self.not_ = not_
        self.predicate_value = predicate_value

    def visit(self, ctx):
        tb = self._get_table_by_clause(ctx)
        idx = tb.index(self.column.value())

        def in_(r):
            v = r[idx] in self.predicate_value.value()
            return not v if self.not_ else v
        return in_


class InPredicateValue(ProxyNode):

    NODE_INDEX = 1


class InValueList(NodeList):
    pass


class ComparisonPredicate(Predicate):

    @classmethod
    def parse(cls, tokens):
        return cls(*tokens)

    def __init__(self, *args):
        self.left, self.op, self.right = args

    def visit(self, ctx):
        # TODO comparition should apply with columns
        tb = self._get_table_by_clause(ctx)
        idx = tb.index(self.left.value())

        def check(r):
            return self.op(r[idx], self.right.value())
        return check
