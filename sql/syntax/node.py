# -*- coding: utf-8 -*-


class Node(object):

    @classmethod
    def parse(cls, prods):
        return cls(prods)

    def visit(self, ctx):
        pass

    def __repr__(self):
        return "<%s>" % self.__class__.__name__


class TokenNode(Node):

    @classmethod
    def parse(cls, prods):
        return cls(prods[0])

    def __init__(self, token):
        self._token = token

    @property
    def name(self):
        return self._token.name

    @property
    def value(self):
        return self._token.value

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.value)
