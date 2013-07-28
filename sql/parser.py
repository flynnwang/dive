# -*- coding: utf-8 -*-

from rply import ParserGenerator

from lexer import TOKENS, sql_lexer
from productions.select import select_core


def build(productions):
    pg = ParserGenerator(TOKENS, cache_id="sql_parser")
    productions(pg)
    return pg.build()


sql_parser = build(lambda pg: select_core(pg))


def parse(sql):
    return sql_parser.parse(sql_lexer.lex(sql))
