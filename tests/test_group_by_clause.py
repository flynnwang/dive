# -*- coding: utf-8 -*-

from testbase import SelectTestBase, DiveTestBase
from itertools import groupby
from dive.sql.parser import parse


class CountFuncTest(SelectTestBase):
    sql = "select count(id) from user"

    def expected_select_result(self):
        return [[len(self.rows)]]

    def test_parse_count_function(self):
        select = parse(self.sql)
        # pylint: disable=E1101
        func_name = select.select_list.selected[0].value
        assert func_name == 'count' 


class SumFuncTest(SelectTestBase):
    sql = "select sum(age) from user"

    def expected_select_result(self):
        return [[sum(r[2] for r in self.rows)]]


class AvgFuncTest(SelectTestBase):
    sql = "select avg(age) from user"

    def expected_select_result(self):
        return [[float(sum(r[2] for r in self.rows))/len(self.rows)]]


class CountAndSumFuncTest(SelectTestBase):
    sql = "select count(age), sum(id) from user"

    def expected_select_result(self):
        return [[len(self.rows), sum(r[0] for r in self.rows)]]


class ColumnCountFuncTest(SelectTestBase):
    sql = "select id, count(id) from user"

    def expected_select_result(self):
        return [[self.rows[0][0], len(self.rows)]]


class SimpleGroupByTest(SelectTestBase):
    sql = "select name, count(id) from user group by name"

    def expected_select_result(self):
        return [[x, len(list(g))] for x, g in
                groupby([r[1] for r in self.rows])]


class GroupByMultipleColumnsTest(SelectTestBase):
    sql = "select id, name, count(id) from user group by id, name"

    def expected_select_result(self):
        return [[x[0], x[1], len(list(g))] for x, g in
                groupby(self.rows, lambda x: (x[0], x[1]))]


class GroupByWithoutAggFuncTest(SelectTestBase):

    sql = "select id, name from user group by id"

    def expected_select_result(self):
        result = []
        for _, g in groupby(self.rows, lambda x: x[0]):
            it = g.next()
            result.append([it[0], it[1]])
        return result
