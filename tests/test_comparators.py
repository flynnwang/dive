# -*- coding: utf-8 -*-

import pytest
from testbase import DiveTestBase


class LessThanCompTest(DiveTestBase):

    sql = 'select id, name, age from user where name < "c"'

    def test_should_find_user_witn_name_before_c(self):
        expected = [r for r in self.rows if r[1] < 'c']
        res = self._execute_query(self.sql)

        assert expected == res
