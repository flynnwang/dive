# -*- coding: utf-8 -*-

import unittest
from . import Table, Schema, Query


class DiveTests(unittest.TestCase):

    def setUp(self):
        table = Table('user', ('id', 'name', 'age'), ['users.csv'])
        self.schema = Schema([table])

    def test_simple_select(self):
        q = Query("select name, age from user", self.schema)
        res = q.execute()

        self.assertEqual(26, len(res))
