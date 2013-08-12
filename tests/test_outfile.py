# -*- coding: utf-8 -*-

import os
import shutil
from testbase import DiveTestBase
from uuid import uuid4
from dive import Query


class OutfileTest(DiveTestBase):

    outfile = "/tmp/" + str(uuid4())
    sql = "select id, name, age into outfile '%s' from user" % outfile

    def setUp(self):
        DiveTestBase.setUp(self)
        os.makedirs(self.outfile)

    def test_outfile(self):
        assert os.path.exists(self.outfile)

        tb = Query(self.sql, self.schema).execute()
        tb.collect()

        assert self._read_csv(self.outfile + '/0000.csv') == self.rows

    def tearDown(self):
        shutil.rmtree(self.outfile)
