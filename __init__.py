# -*- coding: utf-8 -*-

from dpark import DparkContext
from sql.parser import parse

class Table(object):

    def __init__(self, name, fields, paths):
        self.name = name
        self.fields = fields
        self.paths = paths

    def index(self, field):
        return self.fields.index(field)

class Schema(object):

    def __init__(self, tables):
        self.table_dict = {t.name: t for t in tables}

    def find_table(self, name):
        try:
            return self.table_dict[name]
        except :
            raise Exception("table not found: %s" % name)


class Query(object):

    def __init__(self, sql, schema):
        self.sql = sql
        self.schema = schema
        self.dpark = DparkContext()

    def execute(self):
        select = parse(self.sql)
        return select.visit(self)
