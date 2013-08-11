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

    """ I : ;
        I : A;
        I : I A;"""

    @classmethod
    def parse(cls, tokens):
        nodes = cls()
        for t in tokens:
            if type(t) is cls:
                nodes.extend(t)
            elif isinstance(t, Node):
                nodes.append(t)
        return nodes

    def __init__(self):
        super(NodeList, self).__init__()

    def visit(self, ctx):
        for nd in self:
            nd.visit(ctx)

    @property
    def flattened_nodes(self):
        return [self[0]] + self[1]


class OptionalNode(Node):

    """ I : ;
        I : A; """

    @classmethod
    def parse(cls, tokens):
        if tokens:
            return cls([t for t in tokens if isinstance(t, Node)])

    def __init__(self, nodes):
        Node.__init__(self)
        self.nodes = nodes

    def visit(self, ctx):
        for nd in self.nodes:
            nd.visit(ctx)

    @property
    def first(self):
        return self.nodes[0]

#class NodeWrapper(Node):

    #def __init__(self):
        #"""@todo: to be defined1. """
        #Node.__init__(self)

        
