# -*- coding: utf-8 -*-

from rply import Token
from dpark.dependency import Aggregator
from node import Node, TokenNode, NodeList, ProxyNode
from clauses import (GroupByClause, WhereClause, EmptyGroupbyClause,
                     EmptyOrderByClause, EmptyClause)
from functions import Aggregatable
from itertools import izip
from clauses import HavingClause


class SelectExpr(Node):

    @classmethod
    def parse(cls, p):
        where = p[5] or EmptyClause()
        groupby = p[6] or EmptyGroupbyClause()
        having = p[7] or EmptyClause()
        orderby = p[8] or EmptyOrderByClause()
        limit = p[9] or EmptyClause()
        return cls(p[1], p[2], p[4], where, groupby,
                   having, orderby, limit)

    def __init__(self,  select_list, outfile, table_name,
                 where, groupby, having, orderby, limit):
        Node.__init__(self)
        self.select_list = select_list
        self.table_name = table_name
        self.where = where
        self.groupby = groupby
        self.having = having
        self.orderby = orderby
        self.limit = limit
        self.outfile = outfile

    def __repr__(self):
        return "<SelectExpr: SELECT %s FROM %s>" % (self.select_list,
                                                    self.table_name)

    def _apply_where(self, ctx):
        def _map(r):
            return tuple(r[idx] for idx in
                         self.select_list.column_indexes)
        ctx.rdd = ctx.rdd.map(_map)

    def _apply_groupby(self, ctx):
        self.groupby.visit(ctx)

        columns = self.select_list.columns

        def create_combiner(r):
            return tuple(f.create(r)
                         for f, v in izip(columns, r))

        def merge_value(c, v):
            return merge_combiner(c, create_combiner(v))

        def merge_combiner(c1, c2):
            return tuple(f.merge(v1, v2)
                         for f, v1, v2 in izip(columns, c1, c2))

        def make_result((k, r)):
            return tuple(f.result(v) for f, v in izip(columns, r))

        agg = Aggregator(create_combiner, merge_value, merge_combiner)
        ctx.rdd = ctx.rdd.combineByKey(agg).map(make_result)

        self.having.visit(ctx)

    def visit(self, ctx):
        ctx.rdd = ctx.table.rdd(ctx.dpark)
        self.select_list.visit(ctx)
        self.where.visit(ctx)

        if not (self.select_list.has_aggregate_function or
                isinstance(self.groupby, GroupByClause)):
            self._apply_where(ctx)
        else:
            self._apply_groupby(ctx)

        self.limit.visit(ctx)
        self.orderby.visit(ctx)
        return ctx.rdd


class DerivedColumn(ProxyNode):
    pass


class Column(TokenNode, Aggregatable):
    # TODO split up column in select_list and column in agg function

    @property
    def is_agg_func(self):
        return False

    @property
    def name(self):
        return self.token.value

    def value(self, r=None):
        if r:
            return r[self.tb_index]
        return self.token.value

    def create(self, r):
        return self.value(r)

    def _get_table(self, ctx):
        # pylint: disable=E1101
        node = self.parent
        while node:
            if isinstance(node, HavingClause):
                return ctx.result_table
            node = node.parent
        # WhereClause, SelectList
        return ctx.table

    def visit(self, ctx):
        tb = self._get_table(ctx)
        self.tb_index = tb.index(self.name)


class Selectable(object):

    @property
    def has_aggregate_function(self):
        return False

    def column_indexes(self):
        pass

    def column_defs(self, tb):
        pass


class SelectList(ProxyNode):
    pass


# TODO: multi-table support
class Asterisk(TokenNode, Selectable, Aggregatable):

    @property
    def column_indexes(self):
        return range(len(self.tb.columns))

    def column_defs(self, tb):
        return tb.columns.copy()

    @property
    def columns(self):
        # TODO bad design
        columns = [Column(Token('column', c)) for c in self.tb.columns.keys()]
        for c in columns:
            c.tb = self.tb
        return columns

    def visit(self, ctx):
        self.tb = ctx.table
        TokenNode.visit(self, ctx)

    def value(self, r=None):
        return r


class SelectSublist(NodeList, Selectable):

    @property
    def has_aggregate_function(self):
        return any([nd.is_agg_func for nd in self])

    @property
    def column_indexes(self):
        return [c.tb_index for c in self]

    def column_defs(self, tb):
        _type = lambda x: x
        return [(c.name, (tb.columns[c.name]
                if c.name in tb.columns else _type)) for c in self]

    @property
    def columns(self):
        return self


class TableName(TokenNode):
    pass
