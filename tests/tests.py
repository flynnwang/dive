# -*- coding: utf-8 -*-

import unittest
import csv
from dive import Table, Schema, Query
from dive.sql.parser import parse

# TODO: bad to share this, may be broken more tests
SIMPLE_SELECT = "select name from user"
SELECT_WITH_MULTIPLE_COLUMNS = "select id, name from user"
SELECT_WHERE = "select name from user where id=3"


class DiveTests(unittest.TestCase):

    def setUp(self):
        table = Table('user', ('id', 'name', 'age'), ['users.csv'])
        self.schema = Schema([table])
        with open('users.csv', 'r') as f:
            self.lines = [l for l in csv.reader(f)]

    def execute_query(self, sql):
        return Query(sql, self.schema).execute()

    def test_select_with_multiple_columns(self):
        res = self._run_query(SELECT_WITH_MULTIPLE_COLUMNS)
        ids_names = [[r[0], r[1]] for r in self.lines]
        self.assertListEqual(ids_names, res)

    def test_select_where(self):
        res = self._run_query(SELECT_WHERE)
        self.assertEqual(1, len(res))
        self.assertListEqual(["c"], res[0])


class LexerTest(unittest.TestCase):

    def _lex(self, sql):
        return [i.getstr() for i in lex(sql)]

    def test_select_where(self):
        tokens = self._lex(SELECT_WHERE)


class SqlParserText(unittest.TestCase):


    def test_simple_search_condition(self):
        s = parse(SELECT_WHERE)
        expr = s.table_expr.where_clause.search_condition
        self.assertEqual("id", expr.left.value)
        self.assertEqual("3", expr.right.value)


if __name__ == '__main__':
    unittest.main()
