# -*- coding: utf-8 -*-

from testbase import SelectTestBase
from itertools import groupby


class HavingColumnConditionTest(SelectTestBase):
    sql = "select id, count(id) from user groupby id having id < 5"

    def expected_select_result(self):
        return [[id_, len(list(g))]
                for id_, g in groupby(self.rows, lambda x: x[0])
                if id_ < 5]
