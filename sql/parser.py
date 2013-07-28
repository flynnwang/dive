# -*- coding: utf-8 -*-

from rply import ParserGenerator

from lexer import TOKENS, sql_lexer
from productions.select import select_core
from productions.empty import empty


def select_productions(pg):
    select_core(pg)
    empty(pg)
    return pg


def build(productions):
    pg = ParserGenerator(TOKENS, cache_id="sql_parser")
    productions(pg)
    return pg.build()


sql_parser = build(select_productions)


def parse(sql):
    return sql_parser.parse(sql_lexer.lex(sql))
