# -*- coding: utf-8 -*-

import uuid
from dpark import DparkContext, optParser
from sql.parser import parse
from collections import OrderedDict

optParser.add_option("-s")   # "option used for py.test"
optParser.add_option("-x")


class Table(object):

    def __init__(self, name, columns, paths=[], rdd=None):
        self.name = name
        self.columns = OrderedDict(columns)
        self.paths = paths
        self._rdd = rdd

    def index(self, field):
        return self.columns.keys().index(field)

    def rdd(self, dpark=None):
        if self._rdd:
            return self._rdd

        def coercion(r):
            return [conv(r[i]) for i, conv 
                    in enumerate(self.columns.values())]
        return dpark.union([dpark.csvFile(p) for p in self.paths])\
                    .map(coercion)


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

    def execute(self):
        select = parse(self.sql)
        # pylint: disable=E1101
        rdd = select.visit(self)

        name = str(uuid.uuid4())
        columns = select.select_list.columns(self.table)
        result_table = Table(name, columns, rdd=rdd)
        return result_table
