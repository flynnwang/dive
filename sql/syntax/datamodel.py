# -*- coding: utf-8 -*-

from node import TokenNode


class Number(TokenNode):

    def value(self, r=None):
        return int(self.token.value)


class String(TokenNode):

    def value(self, r=None):
        return self.token.value[1:-1]
