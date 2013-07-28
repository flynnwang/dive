# -*- coding: utf-8 -*-

from testbase import DiveTestBase
from dive.sql.parser import parse


class SelectMultiColumnTest(DiveTestBase):

    @property
    def sql(self):
        return "select id, name from user"
       
    def test_should_return_all_id_and_user_name(self):
        res = self._execute_query(self.sql)
        ids_names = [[r[0], r[1]] for r in self.rows]

        assert ids_names == res
