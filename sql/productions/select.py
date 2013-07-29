# -*- coding: utf-8 -*-

from . import Node, IdentifierNode
import where
import columns


def select_core(pg):
    @pg.production("select_core : SELECT result_columns table_expr")
    def _(p):
        _, result_column, table_expr = p
        return SelectCore(result_column, table_expr)

    columns.result_columns(pg)

    @pg.production("table_expr : FROM table_name where_clause")
    def table_expr(p):
        return TableExpr(p[1], p[2])

    @pg.production("table_name : IDENTIFIER")
    def table_name(p):
        return TableName(p[0])

    return where.where_clause(pg)


class SelectCore(Node):

    def __init__(self, columns, table_expr):
        Node.__init__(self)
        self.columns = columns
        self.table_expr = table_expr

    def __repr__(self):
        return "<SelectCore: SELECT %s FROM %s>" % (self.columns,
                                                    self.table_expr)

    def visit(self, ctx):
        ctx.table = ctx.schema.find_table(self.table_expr.table_name.value)
        column_indexes = [ctx.table.index(c.value) for c in self.columns]

        def coercion(r):
            return [conv(r[i]) for i, conv 
                    in enumerate(ctx.table.fields.values())]

        def _map_result(r):
            return [r[idx] for idx in column_indexes]

        ctx.rdd = ctx.dpark\
                     .union([ctx.dpark.csvFile(p) for p in ctx.table.paths])\
                     .map(coercion)

        self.table_expr.visit(ctx)
        return ctx.rdd.map(_map_result).collect()


class TableExpr(Node):

    def __init__(self, table_name, where_clause=None):
        self.table_name = table_name
        self.where_clause = where_clause

    def visit(self, ctx):
        if self.where_clause:
            self.where_clause.visit(ctx)


class TableName(IdentifierNode):
    pass
