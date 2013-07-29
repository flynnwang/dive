# -*- coding: utf-8 -*-

import pytest
from testbase import DiveTestBase


class StringEqualCompTest(DiveTestBase):

    sql = 'select id , name , age from user where name = "c"'

    def test_tokenize_should_parse_string(self):
        tokens = self._tokenize(self.sql)
        expected = '"c"'

        assert expected == tokens[-1]

    def test_should_find_user_witn_name_c(self):
        expected = [r for r in self.rows if r[1] == 'c']
        res = self._execute_query(self.sql)

        assert expected == res


class SingleQuoteStringCompTest(DiveTestBase):

    sql = "select id , name , age from user where name = ' test '"

    def test_tokenize_should_parse_string(self):
        tokens = self._tokenize(self.sql)
        expected = "' test '"

        assert expected == tokens[-1]
