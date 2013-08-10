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


class SelectMultiOrWhereTest(SelectTestBase):
    sql = "select id, name, age from user where id <= 1 or id >= 25"

    def expected_select_result(self):
        return [r for r in self.rows if r[0] <= 1 or r[0] >= 25]


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


class SelectTripleConditionTest(SelectTestBase):
    sql = "select id, name, age from user where id=1 or id=2 or id=3"

    def expected_select_result(self):
        return [r for r in self.rows if r[0] in (1, 2, 3)]
