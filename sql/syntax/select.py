# -*- coding: utf-8 -*-

from node import Node, TokenNode
from conditions import Asterisk


class SelectCore(Node):

    @classmethod
    def parse(cls, prods):
        _, result_column, table_expr = prods
        return cls(prods, result_column, table_expr)

    def __init__(self, p, select_list, table_expr):
        Node.__init__(self, p)
        self.select_list = select_list
        self.table_expr = table_expr

    def __repr__(self):
        return "<SelectCore: SELECT %s FROM %s>" % (self.select_list,
                                                    self.table_expr)

    def visit(self, ctx):
        ctx.table = ctx.schema.find_table(self.table_expr.table_name.value)

        def _map_result(r):
            return [r[idx] for idx in
                    self.select_list.column_indexes(ctx.table)]

        ctx.rdd = ctx.table.rdd(ctx.dpark)
        self.table_expr.visit(ctx)
        return ctx.rdd.map(_map_result)


class Column(TokenNode):

    @classmethod
    def parse(cls, p):
        return Column(p, p[0])


class SelectList(Node, list):

    @classmethod
    def parse(cls, p):
        if len(p) == 1:
            select_list = SelectList(p)
            column = p[0]
        else:
            select_list, _, column = p
        select_list.append(column)
        return select_list

    @property
    def is_select_all(self):
        return len(self) == 1 and isinstance(self[0], Asterisk)

    def column_indexes(self, tb):
        # TODO: multi-table support
        if self.is_select_all:
            return range(len(tb.columns))
        return [tb.index(c.value) for c in self]

    def columns(self, tb):
        """ (name, convter) """
        if self.is_select_all:
            return tb.columns.copy()
        return [(c.value, tb.columns[c.value])
                for c in self if c.value in tb.columns]


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
