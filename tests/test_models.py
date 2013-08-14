# -*- coding: utf-8 -*-

import unittest

from datetime import date
from dive.models import Date


class DateTest(unittest.TestCase):

    def test_date_cast(self):
        date_str = "2013/8/14"
        date_ = Date()

        assert date(2013, 8, 14) == date_.cast(date_str)

    def test_user_defined_date_cast(self):
        date_str = "2013-8-14"
        date_ = Date("%Y-%m-%d")

        assert date(2013, 8, 14) == date_.cast(date_str)
