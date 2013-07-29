# -*- coding: utf-8 -*-

import uuid
from dpark import DparkContext, optParser
from sql.parser import parse
from collections import OrderedDict

optParser.add_option("-s")   # "option used for py.test"
optParser.add_option("-x")


class Table(object):

    def __init__(self, name, fields, paths=[], rdd=None):
        self.name = name
        self.fields = OrderedDict(fields)
        self.paths = paths
        self._rdd = rdd

    def index(self, field):
        return self.fields.keys().index(field)

    def fetch(self, dpark=None):
        return self._rdd.collect() if self.rdd(dpark) else None

    def rdd(self, dpark):
        if self._rdd:
            return self._rdd

        if dpark:
            def coercion(r):
                return [conv(r[i]) for i, conv 
                        in enumerate(self.fields.values())]
            self._rdd = dpark.union([dpark.csvFile(p) for p in self.paths])\
                             .map(coercion)

        return self._rdd


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
        # TODO: rename column name for multiple table?
        fields = [(c.value, self.table.fields[c.value])
                  for c in select.columns]
        return Table(name, fields, rdd=rdd)
