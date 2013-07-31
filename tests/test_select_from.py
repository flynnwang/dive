# -*- coding: utf-8 -*-

from testbase import DiveTestBase, SelectTestBase
from dive.sql.parser import parse


class SelectFromTest(DiveTestBase):

    @property
    def sql(self):
        return "select name from user"
       
    def test_should_return_all_user_names_as_list_of_lists(self):
        res = self._execute_query(self.sql)
        user_names = [[r[1]] for r in self.rows]

        assert user_names == res

    def test_should_return_each_word_as_a_token(self):
        expected = self.sql.split(' ')
        tokens = self._tokenize(self.sql)

        assert expected, tokens

    def test_should_parse_one_column_and_table(self):
        s = parse(self.sql)
        # pylint: disable=E1101
        self.assertEqual(1, len(s.columns))
        self.assertEqual("name", s.columns[0].name)
        self.assertEqual("user", s.table_expr.table_name.name)
