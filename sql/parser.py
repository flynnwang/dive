# -*- coding: utf-8 -*-

from rply import ParserGenerator

from lexer import TOKENS, sql_lexer
from productions.select import select_core
from productions.empty import empty


def build_parser():
    pg = ParserGenerator(TOKENS, cache_id="sql_parser")

    # select-statmanet
    select_core(pg)

    empty(pg)

    return pg.build()


sql_parser = build_parser()


def parse(sql):
    return sql_parser.parse(sql_lexer.lex(sql))
