# -*- coding: utf-8 -*-

import unittest

from datetime import date, time, datetime
from dive.models import Date, Time, Datetime


class DateTest(unittest.TestCase):

    def test_date_cast(self):
        date_str = "2013/8/14"
        date_ = Date()

        assert date(2013, 8, 14) == date_.cast(date_str)

    def test_user_defined_date_cast(self):
        date_str = "2013-8-14"
        date_ = Date("%Y-%m-%d")

        assert date(2013, 8, 14) == date_.cast(date_str)


class TimeTest(unittest.TestCase):

    def test_date_cast(self):
        time_str = "12:02:05"
        time_ = Time()

        assert time(12, 2, 5) == time_.cast(time_str)


class DatetimeTest(unittest.TestCase):

    def test_datetime_cast(self):
        dt_str = "2013/8/14 12:02:05"
        dt_ = Datetime()

        assert datetime(2013, 8, 14, 12, 2, 5) == dt_.cast(dt_str)
