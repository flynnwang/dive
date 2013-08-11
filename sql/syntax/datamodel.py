# -*- coding: utf-8 -*-

from node import TokenNode


class Number(TokenNode):

    def __init__(self, token):
        TokenNode.__init__(self, token)
        self._val = int(token.value)

    @property
    def value(self):
        return self._val


class String(TokenNode):

    def __init__(self, token):
        TokenNode.__init__(self, token)
        self._val = token.value[1:-1]

    @property
    def value(self):
        return self._val
