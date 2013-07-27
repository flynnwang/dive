# -*- coding: utf-8 -*-

import unittest
import csv
from . import Table, Schema, Query
from sql.lexer import lex
from sql.parser import parse


SIMPLE_SELECT = "select name from user"
SELECT_WITH_MULTIPLE_COLUMNS = "select id, name from user"


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


class TestLexer(unittest.TestCase):

    def test_simple_select(self):
        tokens = [i.getstr() for i in lex(SIMPLE_SELECT)]
        expected = SIMPLE_SELECT.split(' ')
        self.assertListEqual(expected, tokens)


class TestSqlParser(unittest.TestCase):

    def test_simple_select(self):
        sc = parse(SIMPLE_SELECT)
        # pylint: disable=E1101
        self.assertEqual(1, len(sc.columns))
        self.assertEqual("name", sc.columns[0].value)
        self.assertEqual("user", sc.table_name.value)


if __name__ == '__main__':
    unittest.main()
