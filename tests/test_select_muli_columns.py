# -*- coding: utf-8 -*-

from testbase import SelectTestBase
from dive.sql.parser import parse


class SelectMultiColumnTest(SelectTestBase):
    sql = "select id, name from user"

    def expected_select_result(self):
        return self._execute_query(self.sql)
