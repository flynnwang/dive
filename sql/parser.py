# -*- coding: utf-8 -*-

from rply import ParserGenerator

from .lexer import TOKENS, sql_lexer

pg = ParserGenerator(TOKENS, cache_id="sql_parser")


@pg.production("select_core : SELECT result_columns table_expr")
def select(p):
    _, result_column, table_name = p
    return SelectCore(result_column, table_name)


@pg.production("table_expr : FROM table_name where_clause")
def table_expr(p):
    return p[1]


@pg.production("where_clause : ")
@pg.production("where_clause : WHERE search_condition")
def where_clause(p):
    return None


@pg.production("search_condition : ")
def search_condition(p):
    return None


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


@pg.production("table_name : IDENTIFIER")
def table_name(p):
    return TableName(p[0])

sql_parser = pg.build()


def parse(sql):
    return sql_parser.parse(sql_lexer.lex(sql))


class Node(object):

    def visit(self, ctx):
        pass


class IdentifierNode(Node):

    def __init__(self, token):
        self.token = token

    @property
    def name(self):
        return self.token.name

    @property
    def value(self):
        return self.token.value

    def __repr__(self):
        return "<IdentifierNode: %s>" % self.value


class ResultColumn(IdentifierNode):
    pass


class ResultColumnGroup(Node, list):

    def __init__(self):
        Node.__init__(self)


class TableName(IdentifierNode):
    pass


class SelectCore(Node):

    def __init__(self, columns, table_name):
        Node.__init__(self)
        self.columns = columns
        self.table_name = table_name

    def __repr__(self):
        return "<SelectCore: SELECT %s FROM %s>" % (self.columns,
                                                    self.table_name)

    def visit(self, ctx):
        table = ctx.schema.find_table(self.table_name.value)
        column_indexes = [table.index(c.value) for c in self.columns]

        def _map_result(r):
            return [r[idx] for idx in column_indexes]

        data = ctx.dpark.union([ctx.dpark.csvFile(p) for p in table.paths])
        return data.map(_map_result).collect()
