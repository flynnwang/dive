# -*- coding: utf-8 -*-

from testbase import SelectTestBase


class SingleColumnDescOrderingTest(SelectTestBase):
    sql = "select * from user order by id desc"

    def expected_select_result(self):
        self.rows.sort(key=lambda r: -r[0])
        return self.rows


class SingleColumnAscOrderingTest(SelectTestBase):
    sql = "select * from user order by id asc"

    def expected_select_result(self):
        self.rows.sort(key=lambda r: r[0])
        return self.rows


class MultiColumnsDescOrderingTest(SelectTestBase):
    sql = "select * from user order by id, name desc"

    def expected_select_result(self):
        self.rows.sort(key=lambda r: (r[0], r[1]), reverse=True)
        return self.rows
