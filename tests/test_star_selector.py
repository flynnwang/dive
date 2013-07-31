# -*- coding: utf-8 -*-

import pytest
from testbase import SelectTestBase


@pytest.skip
class SelectMultiAndWhereTest(SelectTestBase):
    sql = "select * from user"

    def expected_select_result(self):
        return self.rows
