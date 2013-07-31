# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, prods):
        self._prods = prods

    @classmethod
    def parse(cls, prods):
        return cls(prods)

    def visit(self, ctx):
        pass

    def __repr__(self):
        return ("<%s: child(ren)(%s): %s>" % 
               (self.__class__.__name__, len(self._prods), str(self._prods)))


class TokenNode(Node):

    @classmethod
    def parse(cls, prods):
        return cls(prods, prods[0])

    def __init__(self, prods, token):
        Node.__init__(self, prods)
        self._token = token

    @property
    def name(self):
        return self._token.name

    @property
    def value(self):
        return self._token.value

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.value)
