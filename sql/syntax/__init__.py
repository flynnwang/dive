# -*- coding: utf-8 -*-


class Node(object):

    def visit(self, ctx):
        pass


class IdentifierNode(Node):

    def __init__(self, token):
        self.token = token

    @property
    def name(self):
        return self.token.name

    @property
    def value(self):
        return self.token.value

    def __repr__(self):
        return "<IdentifierNode: %s>" % self.value
