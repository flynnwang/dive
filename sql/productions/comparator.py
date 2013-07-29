# -*- coding: utf-8 -*-

import operator as op


def comparator(pg):
    
    @pg.production("comp_op : EQUAL")
    def equal(p):
        return op.eq

    @pg.production("comp_op : LESS_THAN")
    def less_than(p):
        return op.lt

    @pg.production("comp_op : LESS_THAN_OR_EQUAL")
    def less_than_or_equal(p):
        return op.le

    @pg.production("comp_op : GREATER_THAN")
    def greater_than(p):
        return op.gt

    @pg.production("comp_op : GREATER_THAN_OR_EQUAL")
    def greater_than_or_equal(p):
        return op.ge

    return pg
