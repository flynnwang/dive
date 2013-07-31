# -*- coding: utf-8 -*-

from node import Node, TokenNode


class ResultColumn(TokenNode):

    @staticmethod
    def parse(p):
        return ResultColumn(p, p[0])


class ResultColumnGroup(Node, list):

    @staticmethod
    def parse(p):
        if len(p) == 1:
            columns = ResultColumnGroup(p)
            column = p[0]
        else:
            columns, _, column = p
        columns.append(column)
        return columns
