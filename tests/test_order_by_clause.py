# -*- coding: utf-8 -*-

from testbase import SelectTestBase


class SingleColumnDescOrderingTest(SelectTestBase):
    sql = "select * from user order by id desc"

    def expected_select_result(self):
        return tuple(sorted(self.rows, key=lambda r: -r[0]))


class SingleColumnAscOrderingTest(SelectTestBase):
    sql = "select * from user order by id asc"

    def expected_select_result(self):
        return tuple(sorted(self.rows, key=lambda r: r[0]))


class MultiColumnsDescOrderingTest(SelectTestBase):
    sql = "select * from user order by id desc, name asc"

    def expected_select_result(self):
        return tuple(sorted(self.rows, key=lambda r: (r[0], r[1]),
                     reverse=True))
