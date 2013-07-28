# -*- coding: utf-8 -*-

from . import Node, IdentifierNode


def result_columns(pg):

    @pg.production("result_columns : result_column")
    @pg.production("result_columns : result_columns COMMA result_column")
    def result_column_group(p):
        if len(p) == 1:
            columns = ResultColumnGroup()
            column = p[0]
        else:
            columns, _, column = p
        columns.append(column)
        return columns

    @pg.production("result_column : IDENTIFIER")
    def result_column(p):
        return ResultColumn(p[0])


class ResultColumn(IdentifierNode):
    pass


class ResultColumnGroup(Node, list):
    pass
