# -*- coding: utf-8 -*-

from node import TokenNode, Node


class Valueable(object):

    @property
    def is_agg_func(self):
        return False

    @property
    def value(self):
        # TODO: do we need it?
        raise NotImplementedError("should provide a value")


class Number(TokenNode, Valueable):

    def __init__(self, token):
        TokenNode.__init__(self, token)

    @property
    def value(self):
        return int(self.token.value)


class String(TokenNode, Valueable):

    def __init__(self, token):
        TokenNode.__init__(self, token)

    @property
    def value(self):
        return self.token.value[1:-1]
