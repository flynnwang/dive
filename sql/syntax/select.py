# -*- coding: utf-8 -*-

from dpark.dependency import Aggregator
from node import Node, TokenNode, NodeList, WrapNode
from clauses import (GroupByClause, WhereClause, EmptyGroupbyClause,
                     EmptyOrderByClause, EmptyClause)
from functions import Aggregatable
from datamodel import Valueable
from itertools import izip


class SelectExpr(Node):

    @classmethod
    def parse(cls, p):
        outfile = p[2] and p[2].first
        table_name = p[4] 
        where = p[5] and p[5].first or EmptyClause()
        groupby = p[6] and p[6].first or EmptyGroupbyClause()
        having = p[7] and p[7].first or EmptyClause()
        orderby = p[8] and p[8].first or EmptyOrderByClause()
        limit = p[9] and p[9].first
        return cls(p[1], outfile, table_name, where, groupby,
                   having, orderby, limit)

    def __init__(self,  select_list, outfile, table_name,
                 where, groupby, having, orderby, limit):
        self.select_list = select_list
        self.table_name = table_name
        self.where = where
        self.groupby = groupby
        self.having = having
        self.orderby = orderby
        self.limit = limit
        self.outfile = outfile

    def __repr__(self):
        return "<SelectCore: SELECT %s FROM %s>" % (self.select_list,
                                                    self.table_name)

    def _apply_where(self, ctx):
        def _map(r):
            return [r[idx] for idx in
                    self.select_list.column_indexes(ctx.table)]
        ctx.rdd = ctx.rdd.map(_map)

    def _apply_groupby(self, ctx):
        self.groupby.visit(ctx)

        tb = ctx.table
        # TODO: method
        selected = self.select_list.child.flattened_nodes

        # TODO: * support
        def create_combiner(r):
            return [f.create(r[tb.index(f.value)])
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

    def visit(self, ctx):
        ctx.rdd = ctx.table.rdd(ctx.dpark)
        self.where.visit(ctx)

        if not (self.select_list.has_aggregate_function or
                isinstance(self.groupby, GroupByClause)):
            self._apply_where(ctx)
        else:
            self._apply_groupby(ctx)

        self.orderby.visit(ctx)
        return ctx.rdd


class DerivedColumn(WrapNode, Aggregatable):

    def create(self, v):
        return self.child.create(v)

    def merge(self, v1, v2):
        return self.child.merge(v1, v2)

    def result(self, v):
        return self.child.result(v)


# TODO: column -> column_ref (table.column syntax)
class Column(TokenNode, Aggregatable, Valueable):

    @property
    def is_agg_func(self):
        return False

    @property
    def column(self):
        return self._token

    @property
    def name(self):
        return self._token.value

    @property
    def value(self):
        return self._token.value


class Selectable(object):

    @property
    def has_aggregate_function(self):
        return False

    def column_indexes(self, tb):
        pass

    def columns(self, tb):
        pass


class SelectList(WrapNode, Selectable):

    def column_indexes(self, tb):
        return self.child.column_indexes(tb)

    def columns(self, tb):
        return self.child.columns(tb)

    @property
    def has_aggregate_function(self):
        return self.child.has_aggregate_function


# TODO: multi-table support
class Asterisk(TokenNode, Selectable):

    def column_indexes(self, tb):
        return range(len(tb.columns))

    def columns(self, tb):
        return tb.columns.copy()


# TODO: assume only column or agg func
class SelectSublist(NodeList, Selectable):

    @property
    def has_aggregate_function(self):
        return any([nd.child.is_agg_func for nd in self.flattened_nodes])

    def column_indexes(self, tb):
        return [tb.index(c.value) for c in self.flattened_nodes]

    def columns(self, tb):
        _type = lambda x: x
        return [(c.value, (tb.columns[c.value]
                if c.value in tb.columns else _type))
                for c in self.flattened_nodes]


class TableName(TokenNode):
    pass
