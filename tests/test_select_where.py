# -*- coding: utf-8 -*-

from testbase import DiveTestBase
from dive.sql.parser import build
from dive.sql.lexer import TOKENS, sql_lexer
from dive.sql.productions.empty import empty
from dive.sql.productions.where import where_clause


class SelectWhereTest(DiveTestBase):

    @property
    def sql(self):
        return "select name from user where id = 3"

    def test_should_find_user_with_that_id(self):
        row = [r for r in self.rows if r[0] == 3][0]
        res = self._execute_query(self.sql)

        assert 1 == len(res)
        assert row[1] == res[0][0]


class WhereClauseTest(DiveTestBase):

    sql = "where id = 3"

    def test_tokenize_where_clause(self):
        tokens = self._tokenize(self.sql)

        assert ['where', 'id', '=', '3'] == tokens

    def test_parse_search_condition(self):
        parser = build(lambda pg: where_clause(pg))
        where = parser.parse(sql_lexer.lex(self.sql))
        # pylint: disable=E1101
        term = where.search_condition.term

        assert "id" == term.left.value
        assert 3 == term.right.value


class MultiAndWhereTest(DiveTestBase):

    sql = "where id >= 1 and id <= 3"

    def test_tokenize_conditions(self):
        tokens = self._tokenize(self.sql)

        assert ['where', 'id', '>=', '1', 'and', 'id', '<=', '3'] == tokens

    #def test_parse_search_condition(self):
        #parser = build(lambda pg: where_clause(pg))
        #where = parser.parse(sql_lexer.lex(self.sql))
        ## pylint: disable=E1101
        #expr = where.search_condition

        #assert "id" == expr.left.value
        #assert 3 == expr.right.value
