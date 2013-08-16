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

    def value(self, row=None):
        return None

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
        Node.visit(self, ctx)
        return [nd.visit(ctx) for nd in self]

    def value(self, r=None):
        return [v.value(r) for v in self]


class ProxyNode(Node):

    """ ProxyNode propgate method access to the proxied node """

    NODE_INDEX = 0

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[cls.NODE_INDEX])

    def __init__(self, node):
        Node.__init__(self)
        self.node = node

    def value(self, r=None):
        return self.node.value(r)

    def visit(self, ctx):
        Node.visit(self, ctx)
        return self.node.visit(ctx)

    def __getattribute__(self, name):
        if name.startswith('__') and name.endswith('__'):
            return Node.__getattribute__(self, name)
        try:
            return Node.__getattribute__(self, name)
        except:
            return self.node.__getattribute__(name)

    def __repr__(self):
        return "<proxy %s of: %s>" % (self.__class__.__name__,
                                      self.node.__class__.__name__)


class OptionalNode(ProxyNode):

    """ I :  | A; """

    @classmethod
    def parse(cls, tokens):
        return tokens and cls(tokens[0])


class TokenNode(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[0])

    def __init__(self, token):
        Node.__init__(self)
        self.token = token

    def value(self, r=None):
        return self.token.value
