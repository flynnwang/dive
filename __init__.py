# -*- coding: utf-8 -*-

import uuid
from dpark import DparkContext, optParser
from sql.parser import parse
from collections import OrderedDict

optParser.add_option("-s")   # "option used for py.test"
optParser.add_option("-x")


class Table(object):

    def __init__(self, name, columns, paths=[], query=None):
        self.name = name
        self.columns = OrderedDict(columns)
        self.paths = paths
        self.query = query

    def index(self, field):
        return self.columns.keys().index(field)

    def rdd(self, dpark=None):
        if self.query:
            return self.query.rdd

        def coercion(r):
            return [conv(r[i]) for i, conv 
                    in enumerate(self.columns.values())]
        return dpark.union([dpark.csvFile(p) for p in self.paths])\
                    .map(coercion)

    def collect(self):
        rdd = self.query.rdd
        limit = self.query.select.limit
        if limit:
            return rdd.take(limit.value)
        return rdd.collect()


class Schema(object):

    def __init__(self, tables):
        self.table_dict = {t.name: t for t in tables}

    def find_table(self, name):
        try:
            return self.table_dict[name]
        except:
            raise Exception("table not found: %s" % name)


class Query(object):

    def __init__(self, sql, schema):
        self.sql = sql
        self.schema = schema
        self.dpark = DparkContext()
        self.rdd = None

    def execute(self):
        # pylint: disable=E1101
        self.select = parse(self.sql)
        self.table = self.schema.find_table(self.select.table_name.value) 

        name = str(uuid.uuid4())
        columns = self.select.select_list.columns(self.table)
        self.result_table = Table(name, columns, query=self)

        self.select.visit(self)

        return self.result_table
