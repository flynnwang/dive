# -*- coding: utf-8 -*-

import os
import shutil
from testbase import DiveTestBase
from uuid import uuid4
from dive import Query


class OutfileTest(DiveTestBase):

    sql = "select id, name, age into outfile '%s' from user"

    def setUp(self):
        DiveTestBase.setUp(self)
        self.outfile = "/tmp/" + str(uuid4())
        self.sql = self.__class__.sql % self.outfile
        os.makedirs(self.outfile)

    def _expected(self):
        return self.rows

    def test_outfile(self):
        assert os.path.exists(self.outfile)

        tb = Query(self.sql, self.schema).execute()
        tb.collect()

        results = [self._read_csv(os.path.join(self.outfile, f))
                   for f in os.listdir(self.outfile)]
        results = reduce(lambda x, y: x + y, results)
        expected = self._expected()

        assert len(expected) == len(results)
        assert expected == results

    def tearDown(self):
        shutil.rmtree(self.outfile)


class OutfileWithLimitTest(OutfileTest):

    sql = "select id, name, age into outfile '%s' from user limit 5"

    def _expected(self):
        return self.rows[:5]
