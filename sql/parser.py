# -*- coding: utf-8 -*-

from rply import ParserGenerator
from lexer import TOKENS, sql_lexer
from syntax.productions import select_bnf, node_classes
from syntax import gen_productions


def build():
    pg = ParserGenerator(TOKENS, cache_id="sql_parser")
    for prod, cls in gen_productions(select_bnf, node_classes):
        pg.production(prod)(cls.production)
    return pg.build()


sql_parser = build()


def parse(sql):
    return sql_parser.parse(sql_lexer.lex(sql))
