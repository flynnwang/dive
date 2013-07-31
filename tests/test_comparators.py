# -*- coding: utf-8 -*-
from testbase import SelectTestBase


class LessThanCompTest(SelectTestBase):
    sql = 'select id, name, age from user where name < "c"'

    def expected_select_result(self):
        return [r for r in self.rows if r[1] < 'c']


class LessThanOrEqualCompTest(SelectTestBase):
    sql = 'select id, name, age from user where name <= "c"'

    def test_tokenize_should_parse_less_than_or_equal(self):
        lte = self._tokenize(self.sql)
        assert '<=' == lte[-2]

    def expected_select_result(self):
        return [r for r in self.rows if r[1] <= 'c']


class GreaterThanOrEqualCompTest(SelectTestBase):
    sql = 'select id, name, age from user where name >= "y"'

    def test_tokenize_should_parse_greater_than_or_eq(self):
        gt = self._tokenize(self.sql)
        assert '>=' == gt[-2]

    def expected_select_result(self):
        return [r for r in self.rows if r[1] >= 'y']


class GreaterThanCompTest(SelectTestBase):
    sql = 'select id, name, age from user where name > "y"'

    def expected_select_result(self):
        return [r for r in self.rows if r[1] > 'y']


class LikeCompTest(SelectTestBase):
    sql = 'select id, name, age from user where name like "[a-c]"'

    def expected_select_result(self):
        return [r for r in self.rows if 'a' <= r[1] <= 'c']
