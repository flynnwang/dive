# -*- coding: utf-8 -*-

from dpark.dependency import Aggregator
from node import Node, TokenNode
from clauses import (GroupByClause, WhereClause, EmptyGroupbyClause,
                     EmptyOrderByClause, EmptyClause)
from functions import AttributeFunction, AggregateFunction
from itertools import izip


class SelectStatement(Node):

    @classmethod
    def parse(cls, p):
        return cls(p[1], *p[3:])

    def __init__(self,  select_list, table_name, where,
                 groupby, having, orderby, limit):
        self.select_list = select_list
        self.table_name = table_name
        self.where = where and where.first or EmptyClause()
        self.groupby = groupby and groupby.first or EmptyGroupbyClause()
        self.having = having and having.first or EmptyClause()
        self.orderby = orderby and orderby.first or EmptyOrderByClause()
        self.limit = limit and limit.first

    def __repr__(self):
        return "<SelectCore: SELECT %s FROM %s>" % (self.select_list,
                                                    self.table_name)

    def visit(self, ctx):

        def _map_result(r):
            return [r[idx] for idx in
                    self.select_list.column_indexes(ctx.table)]

        ctx.rdd = ctx.table.rdd(ctx.dpark)
        self.where.visit(ctx)

        if not (self.select_list.has_aggregate_function or
                isinstance(self.groupby, GroupByClause)):
            ctx.rdd = ctx.rdd.map(_map_result)
        else:
            self.groupby.visit(ctx)

            tb = ctx.table
            selected = self.select_list.selected

            def create_combiner(r):
                return [f.create(r[tb.index(f.column.value)])
                        for f, v in izip(selected, r)]

            def merge_value(c, v):
                return merge_combiner(c, create_combiner(v))

            def merge_combiner(c1, c2):
                return [f.merge(v1, v2)
                        for f, v1, v2 in izip(selected, c1, c2)]

            def make_result((k, r)):
                return [f.result(v) for f, v in izip(selected, r)]

            agg = Aggregator(create_combiner, merge_value, merge_combiner)
            ctx.rdd = ctx.rdd.combineByKey(agg).map(make_result)

            self.having.visit(ctx)

        self.orderby.visit(ctx)
        return ctx.rdd


class Column(AggregateFunction):

    @classmethod
    def parse(cls, p):
        return Column(p[0])

    def __init__(self, token):
        self._token = token

    @property
    def column(self):
        return self._token

    @property
    def name(self):
        return self._token.value


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
        return SelectList(p[0])

    def __init__(self, selected):
        self.selected = selected

    def column_indexes(self, tb):
        return self.selected.column_indexes(tb)

    def columns(self, tb):
        return self.selected.columns(tb)

    @property
    def has_aggregate_function(self):
        return self.selected.has_aggregate_function


class Asterisk(TokenNode, Selectable):

    def column_indexes(self, tb):
        # TODO: multi-table support
        return range(len(tb.columns))

    def columns(self, tb):
        return tb.columns.copy()


class SelectSublist(Node, Selectable, list):

    @classmethod
    def parse(cls, p):
        sublist = SelectSublist()
        if len(p) == 1:
            column = p[0]
            sublist.append(column)
        else:
            for c in p:
                if isinstance(c, SelectSublist):
                    sublist += c
        return sublist

    @property
    def has_aggregate_function(self):
        return not all([isinstance(c, Column) for c in self])

    def column_indexes(self, tb):
        return [tb.index(c.value) for c in self]

    def columns(self, tb):
        _type = lambda x: x
        return [(c.name, (tb.columns[c.name]
                if c.value in tb.columns else _type))
                for c in self]


class TableName(TokenNode):
    pass
