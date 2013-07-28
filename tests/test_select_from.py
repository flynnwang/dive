# -*- coding: utf-8 -*-

from testbase import DiveTestBase
from dive.sql.parser import parse


class SelectFromTest(DiveTestBase):

    @property
    def sql(self):
        return "select name from user"
       
    def test_should_return_all_user_names_as_list_of_lists(self):
        res = self._execute_query(self.sql)
        user_names = [[r[1]] for r in self.lines]

        assert len(user_names) == len(res)
        assert user_names == res

    def test_should_parse_one_column_and_table(self):
        s = parse(self.sql)
        self.assertEqual(1, len(s.columns))
        self.assertEqual("name", s.columns[0].value)
        self.assertEqual("user", s.table_expr.table_name.value)
