# -*- coding: utf-8 -*-

from testbase import SelectTestBase


class LimitClauseTest(SelectTestBase):
    sql = "select * from user limit 5"

    def expected_select_result(self):
        return self.rows[:5]
