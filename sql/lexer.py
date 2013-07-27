# -*- coding: utf-8 -*-

import rply


class LexerGenerator(rply.LexerGenerator):

    def __init__(self):
        super(LexerGenerator, self).__init__()
        self.tokens = []

    def add(self, name, pattern):
        self.tokens.append(name)
        super(LexerGenerator, self).add(name, pattern)


class LexerGeneratorBuilder(object):

    SQL_KEYWORDS = ['select', 'from', 'where']
    COMPARATORS = [('EQ', '=')]

    IDENTIFIER = ("IDENTIFIER", r"[_a-zA-Z]\w*")
    NUMBER = ("NUMBER", r"\d+")

    def register_keyword_tokens(self, lg):
        for t in self.SQL_KEYWORDS:
            lg.add(t.upper(), t)

    def register_tokens(self, lg, tokens):
        for t, p in tokens:
            lg.add(t.upper(), p)

    def build(self):
        lg = LexerGenerator()

        self.register_keyword_tokens(lg)
        self.register_tokens(lg, self.COMPARATORS)

        lg.add('COMMA', ',')
        lg.add(*self.IDENTIFIER)
        lg.add(*self.NUMBER)
        lg.ignore(r"\s+")
        return lg.tokens, lg.build()

TOKENS, sql_lexer = LexerGeneratorBuilder().build()


def lex(sql):
    stream = sql_lexer.lex(sql)
    while True:
        t = next(stream)
        if not t:
            break
        yield t
