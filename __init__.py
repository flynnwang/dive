# -*- coding: utf-8 -*-

import uuid
import inspect
from dpark import DparkContext, optParser
from sql.parser import parse
from collections import OrderedDict
from models import Model

optParser.add_option("-s")   # "option used for py.test"
optParser.add_option("-x")


class Table(object):

    columns = ()

    def __init__(self, name, paths=None, columns=None, query=None):
        self.name = name
        self.columns = OrderedDict(columns or self.__class__.columns)
        self.paths = paths or []
        self.query = query

    def index(self, field):
        return self.columns.keys().index(field)

    def rdd(self, dpark=None):
        if self.query:
            return self.query.rdd

        def coercion(r):
            return [m.cast(r[i]) for i, m
                    in enumerate(self.columns.values())]
        return dpark.union([dpark.csvFile(p) for p in self.paths])\
                    .map(coercion)

    def collect(self):
        rdd = self.query.rdd

        limit = self.query.select.limit
        if limit:
            rdd = self.query.dpark.makeRDD(rdd.take(limit.value))

        outfile = self.query.select.outfile
        if outfile:
            rdd.saveAsCSVFile(outfile.filedir)
            return outfile.filedir
        return tuple(rdd.collect())


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
        columns = self.select.select_list.column_defs(self.table)
        self.result_table = Table(name, columns=columns, query=self)

        self.select.visit(self)

        return self.result_table
