# -*- coding: utf-8 -*-


class Node(object):

    @classmethod
    def parse(cls, prods):
        return cls(prods)

    @classmethod
    def production(cls, tokens):
        node = cls.parse(tokens)
        for t in tokens:
            if isinstance(t, Node):
                t.parent = node
        return node

    def __init__(self, prods=None):
        self.parent = None

    def visit(self, ctx):
        pass

    def __repr__(self):
        return "<%s>" % self.__class__.__name__


class TokenNode(Node):

    @classmethod
    def parse(cls, prods):
        return cls(prods[0])

    def __init__(self, token):
        super(TokenNode, self).__init__()
        self._token = token

    @property
    def name(self):
        return self._token.name

    @property
    def value(self):
        return self._token.value

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.value)


class NodeList(Node, list):

    @classmethod
    def parse(cls, tokens):
        nodes = cls()
        if len(tokens) == 1:
            nodes, it = cls(), tokens[0]
        else:
            nodes, it = tokens[0], tokens[2]
        nodes.append(it)
        return nodes

    def __init__(self):
        super(NodeList, self).__init__()
