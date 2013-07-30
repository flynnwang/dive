# -*- coding: utf-8 -*-

from testbase import DiveTestBase, SelectTestBase
from dive.sql.parser import build
from dive.sql.lexer import TOKENS, sql_lexer
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
        factor = where.search_condition.term.factor.predicate

        assert "id" == factor.left.value
        assert 3 == factor.right.value


class MultiOrWhereTest(DiveTestBase):

    sql = "where id >= 1 or id <= 3"

    def test_tokenize_conditions(self):
        tokens = self._tokenize(self.sql)

        assert ['where', 'id', '>=', '1', 'or', 'id', '<=', '3'] == tokens

    def test_parse_search_condition(self):
        parser = build(lambda pg: where_clause(pg))
        where = parser.parse(sql_lexer.lex(self.sql))
        # pylint: disable=E1101
        right_factor = where.search_condition.term.factor.predicate

        assert "id" == right_factor.left.value
        assert 3 == right_factor.right.value

        left_factor = where.search_condition.more.term.factor.predicate
        assert "id" == left_factor.left.value
        assert 1 == left_factor.right.value


class SelectMultiOrWhereTest(DiveTestBase):

    sql = "select id, name, age from user where id <= 1 or id >= 25"

    def test_shoud_find_user_with_id_before_1_or_after_25(self):
        rows = [r for r in self.rows if r[0] <= 1 or r[0] >= 25]
        res = self._execute_query(self.sql)

        assert 3 == len(res)
        assert rows == res


class SelectMultiAndWhereTest(DiveTestBase):

    sql = "select id, name, age from user where id >=1 and id <= 3"

    def test_shoud_find_user_with_id_before_1_or_after_25(self):
        rows = [r for r in self.rows if 1 <= r[0] <= 3]
        res = self._execute_query(self.sql)

        assert 3 == len(res)
        assert rows == res


class SelectAndThenOrTest(DiveTestBase):

    sql = "select id, name, age from user where id >=1 and id <= 3 or id >= 20"

    def test_shoud_find_user_with_id_satisfiy_conditions(self):
        rows = [r for r in self.rows if 1 <= r[0] <= 3 or r[0] >= 20]
        res = self._execute_query(self.sql)

        assert rows == res


class SelectNotTest(SelectTestBase):

    sql = "select id, name, age from user where not id >= 3"

    def expected_select_result(self):
        return [r for r in self.rows if not r[0] >= 3]
