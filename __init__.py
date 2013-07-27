# -*- coding: utf-8 -*-

from dpark import DparkContext

class Table(object):

    def __init__(self, name, fields, paths):
        self.name = name
        self.fields = fields

class Schema(object):

    def __init__(self, tables):
        self.tables = tables

class Query(object):

    def __init__(self, schema, sql):
        self.sql = sql
        self.schema = schema
        self.ctx = DparkContext()

    def execute(self):
        return (1, ) * 26
