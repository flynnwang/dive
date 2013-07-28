# -*- coding: utf-8 -*-

from . import Node


def empty(pg):
    @pg.production("empty : ")
    def empty(p):
        return None
