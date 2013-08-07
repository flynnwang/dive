# -*- coding: utf-8 -*-

from rply import ParserGenerator
from lexer import TOKENS, sql_lexer
from syntax import productions


def build():
    pg = ParserGenerator(TOKENS, cache_id="sql_parser")
    for prod, cls in productions:
        prod = prod.split(':', 1)
        name = prod[0].strip()
        exnteds = [p.strip() for p in prod[1].split('|')]

        for p in exnteds:
            production = "%s : %s" % (name, p)
            pg.production(production)(cls.production)
    return pg.build()


sql_parser = build()


def parse(sql):
    return sql_parser.parse(sql_lexer.lex(sql))
