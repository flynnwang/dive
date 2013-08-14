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
        

class Date(object):

    def __init__(self, format="%Y/%m/%d"):
        self.format = format

    def cast(self, s):
        return datetime.strptime(s, self.format).date()
