# -*- coding: utf-8 -*-

from testbase import DiveTestBase, SelectTestBase
from dive.sql.parser import parse


class SelectWhereTest(DiveTestBase):
    sql = "select name from user where id = 3"

    def test_should_find_user_with_that_id(self):
        row = [r for r in self.rows if r[0] == 3][0]
        res = self._execute_query(self.sql)

        assert 1 == len(res)
        assert row[1] == res[0][0]

    def test_parse_search_condition(self):
        select = parse(self.sql)
        # pylint: disable=E1101
        factor = select.table_expr.where_clause\
                       .search_condition.term.factor.predicate

        assert "id" == factor.left.value
        assert 3 == factor.right.value


class SelectMultiOrWhereTest(SelectTestBase):
    sql = "select id, name, age from user where id <= 1 or id >= 25"

    def expected_select_result(self):
        return [r for r in self.rows if r[0] <= 1 or r[0] >= 25]

    def test_parse_search_condition(self):
        select = parse(self.sql)
        # pylint: disable=E1101
        search_condition = select.table_expr.where_clause.search_condition
        right_factor = search_condition.term.factor.predicate
        assert "id" == right_factor.left.value
        assert 25 == right_factor.right.value

        left_factor = search_condition.more.term.factor.predicate
        assert "id" == left_factor.left.value
        assert 1 == left_factor.right.value


class SelectMultiAndWhereTest(SelectTestBase):
    sql = "select id, name, age from user where id >=1 and id <= 3"

    def expected_select_result(self):
        return [r for r in self.rows if 1 <= r[0] <= 3]


class SelectAndThenOrTest(SelectTestBase):
    sql = "select id, name, age from user where id >=1 and id <= 3 or id >= 20"

    def expected_select_result(self):
        return [r for r in self.rows if 1 <= r[0] <= 3 or r[0] >= 20]


class SelectNotTest(SelectTestBase):
    sql = "select id, name, age from user where not id >= 3"

    def expected_select_result(self):
        return [r for r in self.rows if not r[0] >= 3]
