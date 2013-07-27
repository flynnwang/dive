# -*- coding: utf-8 -*-

import unittest
from . import Table, Schema, Query
from sql.lexer import lex
from sql.parser import parse


SIMPLE_SELECT = "select name from user"

class DiveTests(unittest.TestCase):

    def setUp(self):
        table = Table('user', ('id', 'name', 'age'), ['users.csv'])
        self.schema = Schema([table])

    def test_simple_select(self):
        q = Query(SIMPLE_SELECT, self.schema)
        res = q.execute()

        self.assertEqual(26, len(res))


class TestLexer(unittest.TestCase):

    def test_simple_select(self):
        tokens = [i.getstr() for i in lex(SIMPLE_SELECT)]
        expected = SIMPLE_SELECT.split(' ')
        self.assertListEqual(expected, tokens)

class TestSqlParser(unittest.TestCase):

    def test_simple_select(self):
        sc = parse(SIMPLE_SELECT)
        self.assertEqual("name", sc.result_column.value)
        self.assertEqual("user", sc.table_name.value)
