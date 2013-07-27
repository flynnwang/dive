# -*- coding: utf-8 -*-

from rply import ParserGenerator

from .lexer import TOKENS, sql_lexer

pg = ParserGenerator(TOKENS, cache_id="sql_parser")


@pg.production("""select-core :
        SELECT result-column
        FROM table-name""")
def select(p):
    _, result_column, _, join_source = p
    return SelectCore(result_column, join_source)


@pg.production("result-column : IDENTIFIER")
def result_column(p):
    return ResultColumn(p[0])


@pg.production("table-name : IDENTIFIER")
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


class TableName(IdentifierNode):
    pass


class SelectCore(Node):

    def __init__(self, result_column, table_name):
        Node.__init__(self)
        self.result_column = result_column
        self.table_name = table_name

    def __repr__(self):
        return "<SelectCore: SELECT %s FROM %s>" % (self.result_column,
                                                    self.table_name)

    def visit(self, ctx):
        table = ctx.schema.find_table(self.table_name.value)
        col_idx = table.index(self.result_column.value)

        def _map_result(r):
            return r[col_idx]

        data = ctx.dpark.union([ctx.dpark.csvFile(p) for p in table.paths])
        return data.map(_map_result).collect()
