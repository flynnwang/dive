# -*- coding: utf-8 -*-

from testbase import SelectTestBase
from itertools import groupby


class HavingColumnConditionTest(SelectTestBase):
    sql = "select id, count(id) from user groupby id having id < 5"

    def expected_select_result(self):
        return tuple((id_, len(list(g)))
                     for id_, g in groupby(self.rows, lambda x: x[0])
                     if id_ < 5)


class HavingColumnConditionTest2(SelectTestBase):
    sql = "select id, name, count(id) from user groupby id having name < 'c'"

    def expected_select_result(self):
        rows = []
        for id_, g in groupby(self.rows, lambda x: x[0]):
            g = list(g)
            name = g[0][1]
            if name < 'c':
                rows.append((id_, name, len(g)))
        return tuple(rows)
