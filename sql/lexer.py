# -*- coding: utf-8 -*-

import rply


class LexerGenerator(rply.LexerGenerator):

    def __init__(self):
        super(LexerGenerator, self).__init__()
        self.tokens = []

    def add(self, name, pattern):
        self.tokens.append(name)
        super(LexerGenerator, self).add(name, pattern)


KEYWORDS = [
    'select', 'from', 'where', 'like', 'having', 'order', 'not',
    'and', 'or', 'group', 'by', 'desc', 'asc', 'limit', 'into', 'outfile', 'in'
]

SYMBOL_TOKENS = [
    ('EQUAL', '='),
    ('LESS_THAN_OR_EQUAL', '<='),
    ('LESS_THAN', '<'),
    ('GREATER_THAN_OR_EQUAL', '>='),
    ('GREATER_THAN', '>'),
    ('ASTERISK', '[*]'),
    ('LEFT_PAREN', '\('),
    ('RIGHT_PAREN', '\)'),
    ("STRING", r'".*"'),
    ("STRING", r"'.*'"),
    ('COMMA', ','),
    ("IDENTIFIER", r"[_a-zA-Z]\w*"),
    ("NUMBER", r"\d+"),
]


class LexerGeneratorBuilder(object):

    def __init__(self, keywords=KEYWORDS, symbols=SYMBOL_TOKENS):
        self.lg = LexerGenerator()
        self.keywords = keywords
        self.symbols = symbols

    def register_keywords(self, keywords):
        for t in keywords:
            self.lg.add(t.upper(), t)

    def register_symbols(self, symbols):
        for t, p in symbols:
            self.lg.add(t.upper(), p)

    def build(self):
        self.register_keywords(self.keywords)
        self.register_symbols(self.symbols)
        self.lg.ignore(r"\s+")
        return self.lg.tokens, self.lg.build()

TOKENS, sql_lexer = LexerGeneratorBuilder().build()


def lex(s, lexer=sql_lexer):
    stream = lexer.lex(s)
    while True:
        t = next(stream)
        if not t:
            break
        yield t
