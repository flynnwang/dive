# -*- coding: utf-8 -*-

import rply
from collections import defaultdict
from node import Node, NodeList

TOKENS = {
    'IDENT': r'[a-zA-Z]\w*',
    'OPEN_BRACKET': r'\[',  # optinal
    'CLOSE_BRACKET': r'\]',
    'OR': r'\|',
    'OPEN_BRACE': r'{',     # one or more
    'CLOSE_BRACE': r'}',
    'COLON': r':',
    'SEMICOLON': r';'
}

lexer_gen = rply.LexerGenerator()
for t, r in TOKENS.items():
    lexer_gen.add(t, r)
lexer_gen.ignore(r"\s+")
bnf_lexer = lexer_gen.build()


class ProductionList(NodeList):

    def visit(self, prods):
        for p in self:
            p.visit(prods)


class Production(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[0], tokens[2])

    def __init__(self, ident, alternatives):
        self.ident = ident
        self.alternatives = alternatives

    def visit(self, prods):
        #for it in self.item_list:
            #it.visit(prods, self.ident.value)
        pass


class Alternatives(NodeList):
    pass


class ItemList(NodeList):

    def visit(self, prods, ident_val):
        for i, it in enumerate(self):
            item_ident = "%s_%s" % (ident_val, i)
            prods[ident_val].append(item_ident)
            it.visit(prods, item_ident)


class SurroundItems(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[1])

    def __init__(self, item_list):
        Node.__init__(self)
        self.item_list = item_list


class OptionalItems(SurroundItems):
    pass


class RepetitiveItems(SurroundItems):
    pass


class Identifier(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[0])

    def __init__(self, token):
        Node.__init__(self)
        self.token = token

    @property
    def value(self):
        return self.token.value

    def visit(self, prods, ident_val):
        pass


class EmptyItem(Node):

    @classmethod
    def parse(cls, tokens):
        return None
        
        
productions = (
    ('production_list : production', ProductionList),
    ('production_list : production_list production', ProductionList),

    ('production : IDENT COLON alternatives SEMICOLON', Production),

    ('alternatives : item_list', Alternatives),
    ('alternatives : item_list OR item_list', Alternatives),

    ('item_list : item', ItemList),
    ('item_list : item_list item', ItemList),

    ('item : ', EmptyItem),
    ('item : IDENT', Identifier),
    ('item : OPEN_BRACKET item_list CLOSE_BRACKET', OptionalItems),
    ('item : OPEN_BRACE item_list CLOSE_BRACE', RepetitiveItems),
)


parser_gen = rply.ParserGenerator(TOKENS.keys(), cache_id="bnf_parser")
for prod, cls in productions:
    parser_gen.production(prod)(cls.production)
bnf_parser = parser_gen.build()


#def gen_productions(bnf):
    #production_list = bnf_parser.parse(bnf_lexer.lex(bnf))
    #prods = defaultdict(list)
    ## pylint: disable=E1101
    #production_list.visit(prods)
    #return prods
