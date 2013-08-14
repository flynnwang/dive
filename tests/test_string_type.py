# -*- coding: utf-8 -*-

import pytest
from testbase import SelectTestBase, DiveTestBase


class StringEqualCompTest(SelectTestBase):
    sql = 'select id , name , age from user where name = "c"'

    def test_tokenize_should_parse_string(self):
        tokens = self._tokenize(self.sql)
        expected = '"c"'

        assert expected == tokens[-1]

    def expected_select_result(self):
        return tuple(r for r in self.rows if r[1] == 'c')


class SingleQuoteStringCompTest(DiveTestBase):

    sql = "select id , name , age from user where name = ' test '"

    def test_tokenize_should_parse_string(self):
        tokens = self._tokenize(self.sql)
        expected = "' test '"

        assert expected == tokens[-1]
