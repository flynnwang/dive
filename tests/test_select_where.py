# -*- coding: utf-8 -*-

from testbase import DiveTestBase
from dive.sql.parser import parse
from dive.sql.lexer import lex


class SelectWhereTest(DiveTestBase):

    @property
    def sql(self):
        return "select name from user where id = 3"
       
    def test_tokenize_where_clause(self):
        tokens = self._tokenize('where id = 3')

        assert ['where', 'id', '=', '3'] == tokens

    def test_parse_search_condition(self):
        # TODO: generate a partical parser for where clause
        s = parse(self.sql)
        expr = s.table_expr.where_clause.search_condition
        self.assertEqual("id", expr.left.value)
        self.assertEqual("3", expr.right.value)

    def test_should_find_user_with_that_id(self):
        row = [r for r in self.rows if r[0] == '3'][0]
        res = self._execute_query(self.sql)

        assert 1 == len(res)
        assert row[1] == res[0][0]

