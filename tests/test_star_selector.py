# -*- coding: utf-8 -*-

import pytest
from testbase import SelectTestBase


class SelectMultiAndWhereTest(SelectTestBase):
    sql = "select * from user"

    def expected_select_result(self):
        return self.rows
