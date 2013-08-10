# -*- coding: utf-8 -*-
from testbase import SelectTestBase


class InPredicateTest(SelectTestBase):
    sql = 'select id, name, age from user where id in (1, 2, 3)'

    def expected_select_result(self):
        return [r for r in self.rows if r[0] in (1, 2, 3)]


class NotInPredicateTest(SelectTestBase):
    sql = 'select id, name, age from user where id not in (1, 2, 3)'

    def expected_select_result(self):
        return [r for r in self.rows if r[0] not in (1, 2, 3)]
