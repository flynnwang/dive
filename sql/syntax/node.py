# -*- coding: utf-8 -*-


class Node(object):

    @classmethod
    def parse(cls, tokens):
        raise NotImplementedError()

    @classmethod
    def production(cls, tokens):
        node = cls.parse(tokens)
        for t in tokens:
            if isinstance(t, Node):
                t.parent = node
        return node

    def visit(self, ctx):
        pass

    def __repr__(self):
        return "<%s>" % self.__class__.__name__


class NodeList(Node, list):

    """ I : A | I A; """

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
        return [nd.visit(ctx) for nd in self]

    @property
    def value(self):
        return [v.value for v in self]


class OptionalNode(Node):

    """ I :  | A; """

    @classmethod
    def parse(cls, tokens):
        return tokens and cls([t for t in tokens if isinstance(t, Node)])

    def __init__(self, nodes):
        Node.__init__(self)
        self.nodes = nodes

    def visit(self, ctx):
        for nd in self.nodes:
            nd.visit(ctx)

    @property
    def first(self):
        return self.nodes[0]


class ProxyNode(Node):

    """ ProxyNode propgate method access to the proxied node """

    NODE_INDEX = 0

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[cls.NODE_INDEX])

    def __init__(self, node):
        Node.__init__(self)
        self.node = node

    @property
    def value(self):
        return self.node.value

    def visit(self, ctx):
        return self.node.visit(ctx)

    def __getattribute__(self, name):
        if name.startswith('__') and name.endswith('__'):
            return Node.__getattribute__(self, name)
        try:
            return Node.__getattribute__(self, name)
        except:
            return self.node.__getattribute__(name)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__,
                             self.node.__class__.__name__)


class TokenNode(ProxyNode):

    def __init__(self, token):
        super(TokenNode, self).__init__(token)

    @property
    def token(self):
        return self.node
