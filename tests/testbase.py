# -*- coding: utf-8 -*-


from os.path import dirname, abspath, join
import unittest
import csv
from dive import Table, Schema, Query
from dive.sql.lexer import lex


class DiveTestBase(unittest.TestCase):

    @property
    def sql(self):
        """ sub class provide sql"""
        return ""

    def setUp(self):
        users_file_path = join(dirname(abspath(__file__)), 'users.csv')
        table = Table('user', ('id', 'name', 'age'), [users_file_path])
        self.schema = Schema([table])
        with open(users_file_path, 'r') as f:
            self.rows = [l for l in csv.reader(f)]

    def _execute_query(self, sql):
        return Query(sql, self.schema).execute()

    def _tokenize(self, s):
        return [i.getstr() for i in lex(s)]
