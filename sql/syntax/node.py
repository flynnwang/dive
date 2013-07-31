# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, prods):
        self._prods = prods

    @classmethod
    def parse(cls, prods):
        return cls(prods)

    def visit(self, ctx):
        pass


class TokenNode(Node):

    @classmethod
    def parse(cls, prods):
        try:
            return cls(prods, prods[0])
        except Exception, e:
            print cls
            raise e

    def __init__(self, prods, token):
        Node.__init__(self, prods)
        self._token = token

    @property
    def name(self):
        return self._token.value

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)
