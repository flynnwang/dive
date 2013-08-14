# -*- coding: utf-8 -*-

from datetime import datetime


class Model(object):

    def cast(self, s):
        raise NotImplementedError()
        

class String(Model):

    def cast(self, s):
        return s


class Integer(Model):

    def cast(self, s):
        return int(s)


class Float(Model):

    def cast(self, s):
        return float(s)
        

class Date(Model):

    def __init__(self, format="%Y/%m/%d"):
        self.format = format

    def cast(self, s):
        return datetime.strptime(s, self.format).date()


class Time(Model):

    def __init__(self, format="%H:%M:%S"):
        self.format = format

    def cast(self, s):
        return datetime.strptime(s, self.format).time()


class Datetime(Model):

    def __init__(self, format="%Y/%m/%d %H:%M:%S"):
        self.format = format

    def cast(self, s):
        return datetime.strptime(s, self.format)
