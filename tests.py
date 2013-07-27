# -*- coding: utf-8 -*-

import unittest
import csv
from . import Table, Schema, Query
from sql.lexer import lex
from sql.parser import parse

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

    def _run_query(self, sql):
        return Query(sql, self.schema).execute()

    def test_simple_select(self):
        res = self._run_query(SIMPLE_SELECT)
        self.assertEqual(len(self.lines), len(res))

        user_names = [[r[1]] for r in self.lines]
        self.assertListEqual(user_names, res)

    def test_select_with_multiple_columns(self):
        res = self._run_query(SELECT_WITH_MULTIPLE_COLUMNS)
        ids_names = [[r[0], r[1]] for r in self.lines]
        self.assertListEqual(ids_names, res)

    def test_select_where(self):
        res = self._run_query(SELECT_WHERE)
        self.assertEqual(1, len(res))
        self.assertListEqual(["c"], res[0])


class TestLexer(unittest.TestCase):

    def _lex(self, sql):
        return [i.getstr() for i in lex(sql)]

    def test_simple_select(self):
        tokens = self._lex(SIMPLE_SELECT)
        expected = SIMPLE_SELECT.split(' ')
        self.assertListEqual(expected, tokens)

    def test_select_where(self):
        tokens = self._lex(SELECT_WHERE)


class TestSqlParser(unittest.TestCase):

    def test_simple_select(self):
        sc = parse(SIMPLE_SELECT)
        # pylint: disable=E1101
        self.assertEqual(1, len(sc.columns))
        self.assertEqual("name", sc.columns[0].value)
        self.assertEqual("user", sc.table_expr.table_name.value)

    def test_simple_search_condition(self):
        s = parse(SELECT_WHERE)
        expr = s.table_expr.where_clause.search_condition
        self.assertEqual("id", expr.left.value)
        self.assertEqual("3", expr.right.value)


if __name__ == '__main__':
    unittest.main()
