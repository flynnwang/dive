# -*- coding: utf-8 -*-

from dpark.dependency import Aggregator
from node import Node, TokenNode
from functions import AttributeFunction
from itertools import izip



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

        if not self.select_list.has_aggregate_function:
            return ctx.rdd.map(_map_result)

        # group by & agg function
        # current only one function with empty group
        tb = ctx.table
        selected = self.select_list.selected

        def create_combiner(r):
            return [f.create(r[tb.index(f.column.value)])
                    for f, v in izip(selected, r)]

        def merge_value(c, v):
            return merge_combiner(c, create_combiner(v))

        def merge_combiner(c1, c2):
            return [f.merge(v1, v2) for f, v1, v2 in izip(selected, c1, c2)]

        def make_result((k, r)):
            return [f.result(v) for f, v in izip(selected, r)]

        agg = Aggregator(create_combiner, merge_value, merge_combiner)
        return ctx.rdd.map(lambda r: (None, r))\
                  .combineByKey(agg)\
                  .map(make_result)


class Column(TokenNode):

    @classmethod
    def parse(cls, p):
        return Column(p, p[0])


class Selectable(object):

    @property
    def has_aggregate_function(self):
        return False

    def column_indexes(self, tb):
        pass

    def columns(self, tb):
        pass


class SelectList(Node, Selectable):

    @classmethod
    def parse(cls, p):
        return SelectList(p, p[0])

    def __init__(self, prods, selected):
        Node.__init__(self, prods)
        self.selected = selected

    def column_indexes(self, tb):
        return self.selected.column_indexes(tb)

    def columns(self, tb):
        return self.selected.columns(tb)

    @property
    def has_aggregate_function(self):
        return self.selected.has_aggregate_function


class Asterisk(Node, Selectable):

    def column_indexes(self, tb):
        # TODO: multi-table support
        return range(len(tb.columns))

    def columns(self, tb):
        return tb.columns.copy()


class SelectSubList(Node, Selectable, list):

    @classmethod
    def parse(cls, p):
        sublist = SelectSubList(p)
        if len(p) == 1:
            column = p[0]
            sublist.append(column)
        else:
            for c in p:
                if isinstance(c, SelectSubList):
                    sublist += c
        return sublist

    @property
    def has_aggregate_function(self):
        return any([True for c in self if isinstance(c, AttributeFunction)])

    def column_indexes(self, tb):
        return [tb.index(c.value) for c in self]

    def columns(self, tb):
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
