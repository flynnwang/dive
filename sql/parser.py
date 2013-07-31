# -*- coding: utf-8 -*-

from rply import ParserGenerator
from lexer import TOKENS, sql_lexer
from syntax import productions


def build():
    pg = ParserGenerator(TOKENS, cache_id="sql_parser")
    for prod, cls in productions:
        pg.production(prod)(cls.parse)
    return pg.build()


sql_parser = build()


def parse(sql):
    return sql_parser.parse(sql_lexer.lex(sql))
