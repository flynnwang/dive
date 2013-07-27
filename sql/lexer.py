# -*- coding: utf-8 -*-

import rply

SQL_KEYWORDS = ['select', 'from']

IDENTIFIER = ("IDENTIFIER", r"[_a-zA-Z]\w*")


class LexerGenerator(rply.LexerGenerator):

    def __init__(self):
        super(LexerGenerator, self).__init__()
        self.tokens = []

    def add(self, name, pattern):
        self.tokens.append(name)
        super(LexerGenerator, self).add(name, pattern)


class LexerGeneratorBuilder(object):

    def __init__(self, keywords):
        self.keywords = keywords

    def register_keyword_tokens(self, lg):
        for k in SQL_KEYWORDS:
            lg.add(k.upper(), k)

    def build(self):
        lg = LexerGenerator()

        self.register_keyword_tokens(lg)
        lg.add('COMMA', ',')
        lg.add(*IDENTIFIER)
        lg.ignore(r"\s+")
        return lg.tokens, lg.build()

TOKENS, sql_lexer = LexerGeneratorBuilder(SQL_KEYWORDS).build()


def lex(sql):
    stream = sql_lexer.lex(sql)
    while True:
        t = next(stream)
        if not t:
            break
        yield t
