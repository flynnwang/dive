# -*- coding: utf-8 -*-

from node import TokenNode


class Number(TokenNode):

    @property
    def value(self):
        return int(self.token.value)


class String(TokenNode):

    @property
    def value(self):
        return self.token.value[1:-1]
