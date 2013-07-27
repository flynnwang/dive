# -*- coding: utf-8 -*-

from rply import ParserGenerator

from .lexer import TOKENS, sql_lexer

pg = ParserGenerator(TOKENS, cache_id="sql_parser")


@pg.production("select_core : SELECT result_columns table_expr")
def select(p):
    _, result_column, table_expr = p
    return SelectCore(result_column, table_expr)


@pg.production("table_expr : FROM table_name where_clause")
def table_expr(p):
    return TableExpr(p[1], p[2])


@pg.production("where_clause : WHERE search_condition")
@pg.production("where_clause : empty")
def where_clause(p):
    return p[0] is not None and WhereClause(p[1])


@pg.production("search_condition : ")
@pg.production("search_condition : boolean_expr")
def search_condition(p):
    return p[0]


@pg.production("""boolean_expr :
        row_value_designator comp_op row_value_designator""")
def boolean_expr(p):
    return BooleanExpr(*p)


@pg.production("row_value_designator : IDENTIFIER")
def row_value_designator(p):
    return RowValueDesignator(p[0])


@pg.production("row_value_designator : NUMBER")
def row_value_designator(p):
    return Number(p[0])


@pg.production("comp_op : EQ")
def comp_op(p):
    return EqualOperator()


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


@pg.production("empty : ")
def empty(p):
    return None


sql_parser = pg.build()


def parse(sql):
    return sql_parser.parse(sql_lexer.lex(sql))


class Node(object):

    def visit(self, ctx):
        pass


class Clause(Node):
    pass


class WhereClause(Clause):

    def __init__(self, search_condition):
        self.search_condition = search_condition

    def visit(self, ctx):
        self.search_condition.visit(ctx)


class Predicate(Node):
    pass


class BooleanExpr(Predicate):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def visit(self, ctx):
        idx = ctx.table.index(self.left.value)
        ctx.data = ctx.data.filter(lambda r: self.op(r[idx], self.right.value))


class Comparator(Node):

    def __call__(self):
        pass


class EqualOperator(Comparator):

    def __call__(self, left, right):
        return left == right


class Number(Node):

    def __init__(self, token):
        self.token = token
        self.value = token.value


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


class RowValueDesignator(IdentifierNode):
    pass


class TableExpr(Node):

    def __init__(self, table_name, where_clause=None):
        self.table_name = table_name
        self.where_clause = where_clause
        print self.where_clause

    def visit(self, ctx):
        if self.where_clause:
            self.where_clause.visit(ctx)


class SelectCore(Node):

    def __init__(self, columns, table_expr):
        Node.__init__(self)
        self.columns = columns
        self.table_expr = table_expr

    def __repr__(self):
        return "<SelectCore: SELECT %s FROM %s>" % (self.columns,
                                                    self.table_expr)

    def visit(self, ctx):
        table = ctx.schema.find_table(self.table_expr.table_name.value)
        column_indexes = [table.index(c.value) for c in self.columns]

        def _map_result(r):
            return [r[idx] for idx in column_indexes]

        ctx.table = table
        ctx.data = ctx.dpark.union([ctx.dpark.csvFile(p) for p in table.paths])
        #print self.table_expr, type(self.table_expr)
        self.table_expr.visit(ctx)
        return ctx.data.map(_map_result).collect()
