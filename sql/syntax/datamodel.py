# -*- coding: utf-8 -*-

from node import TokenNode


class Number(TokenNode):

    def __init__(self, token):
        TokenNode.__init__(self, token)

    @property
    def value(self):
        return int(self._token.value)


class String(TokenNode):

    def __init__(self, token):
        TokenNode.__init__(self, token)

    @property
    def value(self):
        return self._token.value[1:-1]
