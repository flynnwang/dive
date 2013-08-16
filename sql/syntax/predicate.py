# -*- coding: utf-8 -*-

import re
from node import Node, NodeList, ProxyNode
from clauses import WhereClause, HavingClause


class Predicate(ProxyNode):
    pass


class LikePredicate(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(column=tokens[0], not_=tokens[1], pattern=tokens[3])

    def __init__(self, column, not_, pattern):
        Node.__init__(self)
        self.column = column
        self.not_ = not_
        self.pattern = re.compile(pattern.value())

    def visit(self, ctx):
        self.column.visit(ctx)

        def like_(r):
            v = self.pattern.match(self.column.value(r))
            return not v if self.not_ else v
        return like_


class InPredicate(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(column=tokens[0], not_=tokens[1], predicate_value=tokens[3])

    def __init__(self, column, not_, predicate_value):
        Node.__init__(self)
        self.column = column
        self.not_ = not_
        self.predicate_value = predicate_value

    def visit(self, ctx):
        self.column.visit(ctx)

        def in_(r):
            v = self.column.value(r) in self.predicate_value.value()
            return not v if self.not_ else v
        return in_


class InPredicateValue(ProxyNode):

    NODE_INDEX = 1


class InValueList(NodeList):
    pass


class ComparisonPredicate(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(*tokens)

    def __init__(self, *args):
        self.left, self.op, self.right = args

    def visit(self, ctx):
        self.left.visit(ctx)
        self.right.visit(ctx)

        def check(r):
            return self.op(self.left.value(r), self.right.value(r))
        return check
