# -*- coding: utf-8 -*-

from testbase import SelectTestBase, DiveTestBase
from itertools import groupby
from dive.sql.parser import parse


class CountFuncTest(SelectTestBase):
    sql = "select count(id) from user"

    def expected_select_result(self):
        return [[len(self.rows), ]]

    def test_parse_count_function(self):
        select = parse(self.sql)
        # pylint: disable=E1101
        func_name = select.select_list[0].value
        assert func_name == 'count' 


#class SimpleGroupByTest(SelectTestBase):
    #sql = "select count(id) from user group by name"

    #def expected_select_result(self):
        #return [len(list(g)) for _, g in groupby([r[1] for r in self.rows])]
