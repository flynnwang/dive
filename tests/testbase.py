# -*- coding: utf-8 -*-


from os.path import dirname, abspath, join
import unittest
import csv
from dive import Table, Schema, Query
from dive.sql.lexer import lex


class DiveTestBase(unittest.TestCase):

    @property
    def sql(self):
        """ sub class provide sql detail"""
        return ""

    def setUp(self):
        users_file_path = join(dirname(abspath(__file__)), 'users.csv')
        table = Table('user', ('id', 'name', 'age'), [users_file_path])
        self.schema = Schema([table])
        with open(users_file_path, 'r') as f:
            self.lines = [l for l in csv.reader(f)]

    def test_should_return_each_word_as_a_token(self):
        expected = self.sql.split(' ')
        tokens = [i.getstr() for i in lex(self.sql)]

        assert expected, tokens

    def _execute_query(self, sql):
        return Query(sql, self.schema).execute()

