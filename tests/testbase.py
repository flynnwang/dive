# -*- coding: utf-8 -*-

import pytest
from os.path import dirname, abspath, join
import unittest
import csv
from dive import Table, Schema, Query
from dive.sql.lexer import lex


class UserTable(Table):

    def __init__(self, paths):
        name = "user"
        fields = [("id", int), ("name", str), ("age", int)]
        Table.__init__(self, name, fields, paths)


class DiveTestBase(unittest.TestCase):

    @property
    def sql(self):
        """ sub class provide sql"""
        return ""

    test_file_path = join(dirname(abspath(__file__)), 'users.csv')

    def setUp(self):
        table = UserTable([self.test_file_path])
        self.schema = Schema([table])
        self.rows = self._read_csv(self.test_file_path)

    def _read_csv(self, filepath):
        with open(filepath, 'r') as f:
            rows = [[int(l[0]), l[1], int(l[2])] for l in csv.reader(f)]
        return rows

    def _execute_query(self, sql):
        tb = Query(sql, self.schema).execute()
        return tb.collect()

    def _tokenize(self, s):
        return [i.getstr() for i in lex(s)]


class SelectTestBase(DiveTestBase):

    sql = "select id, name, age from user"

    def expected_select_result(self):
        return self.rows

    def test_should_return_expected_results(self):
        expected = self.expected_select_result()
        res = self._execute_query(self.sql)
        assert expected == res
