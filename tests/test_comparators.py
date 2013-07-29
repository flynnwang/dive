# -*- coding: utf-8 -*-

import pytest
from testbase import DiveTestBase


class LessThanCompTest(DiveTestBase):

    sql = 'select id, name, age from user where name < "c"'

    def test_should_find_user_witn_name_before_c(self):
        expected = [r for r in self.rows if r[1] < 'c']
        res = self._execute_query(self.sql)

        assert expected == res


class LessThanOrEqualCompTest(DiveTestBase):

    sql = 'select id, name, age from user where name <= "c"'

    def test_tokenize_should_parse_less_than_or_equal(self):
        lte = self._tokenize(self.sql)
        assert '<=' == lte[-2]

    def test_should_find_user_witn_name_smaller_than_or_equal_c(self):
        expected = [r for r in self.rows if r[1] <= 'c']
        res = self._execute_query(self.sql)

        assert expected == res


class GreaterThanOrEqualCompTest(DiveTestBase):

    sql = 'select id, name, age from user where name >= "y"'

    def test_tokenize_should_parse_greater_than_or_eq(self):
        gt = self._tokenize(self.sql)
        assert '>=' == gt[-2]

    def test_should_find_user_witn_name_y_or_after(self):
        expected = [r for r in self.rows if r[1] >= 'y']
        res = self._execute_query(self.sql)

        assert expected == res


class GreaterThanCompTest(DiveTestBase):

    sql = 'select id, name, age from user where name > "y"'

    def test_should_find_user_witn_name_after_y(self):
        expected = [r for r in self.rows if r[1] > 'y']
        res = self._execute_query(self.sql)

        assert expected == res
