# -*- coding: utf-8 -*-

from node import Node, TokenNode


class SelectCore(Node):

    @classmethod
    def parse(cls, prods):
        _, result_column, table_expr = prods
        return cls(prods, result_column, table_expr)

    def __init__(self, p, columns, table_expr):
        Node.__init__(self, p)
        self.columns = columns
        self.table_expr = table_expr

    def __repr__(self):
        return "<SelectCore: SELECT %s FROM %s>" % (self.columns,
                                                    self.table_expr)

    def visit(self, ctx):
        ctx.table = ctx.schema.find_table(self.table_expr.table_name.value)
        column_indexes = [ctx.table.index(c.value) for c in self.columns]

        def _map_result(r):
            return [r[idx] for idx in column_indexes]

        ctx.rdd = ctx.table.rdd(ctx.dpark)
        self.table_expr.visit(ctx)
        return ctx.rdd.map(_map_result)


class TableExpr(Node):

    @classmethod
    def parse(cls, p):
        return TableExpr(p, p[1], p[2])

    def __init__(self, p, table_name, where_clause=None):
        Node.__init__(self, p)
        self.table_name = table_name
        self.where_clause = where_clause

    def visit(self, ctx):
        if self.where_clause:
            self.where_clause.visit(ctx)


class TableName(TokenNode):
    pass
