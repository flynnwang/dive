# -*- coding: utf-8 -*-

import rply
from collections import defaultdict
from node import Node, TokenNode, NodeList

TOKENS = {
    'IDENT': r'[a-zA-Z]\w*',
    'OPEN_BRACKET': r'\[',  # optinal
    'CLOSE_BRACKET': r'\]',
    'OR': r'\|',
    'OPNE_BRACE': r'{',     # one or more
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

    def __init__(self, ident, item_list):
        self.ident = ident
        self.item_list = item_list

    def visit(self, prods):
        for it in self.item_list:
            it.visit(prods, self.ident.value)


class ItemList(NodeList):

    def visit(self, prods, ident_val):
        for i, it in enumerate(self):
            item_ident = "%s_%s" % (ident_val, i)
            prods[ident_val].append(item_ident)
            it.visit(prods, item_ident)


class Item(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[0])

    def __init__(self, it):
        Node.__init__(self)
        self.it = it

    def visit(self, prods, ident_val):
        pass


class OptionalItem(Item):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[1])

    def __init__(self, item_list):
        Item.__init__(self)
        self.item_list = item_list


class RepetitiveItem(Item):
        
    @classmethod
    def parse(cls, tokens):
        return cls(tokens[1])

    def __init__(self, item_list):
        Item.__init__(self)
        self.item_list = item_list
        
p = (
    ('production_list : production', ProductionList),
    ('production_list : production_list SEMICOLON production', ProductionList),

    ('production : IDENT COLON item_of_choise SEMICOLON', Production),

    ('item_of_choise : item_list', ItemList),
    ('item_of_choise : item_list OR item_list', ItemList),
    ('item_list : item', ItemList),
    ('item_list : item_list item', ItemList),

    ('item : optinal_item', Item),
    ('item : repetitive_item', Item),
    ('item : IDENT', Item),
    ('optional_item : OPEN_BRACKET item_list CLOSE_BRACKET', OptionalItem),
    ('repetitive_item : OPEN_BRACE item_list CLOSE_BRACE', RepetitiveItem),
)


#parser_gen = rply.ParserGenerator(TOKENS.keys(), cache_id="bnf_parser")
#for prod, cls in p:
    #parser_gen.production(prod)(cls.production)
#bnf_parser = parser_gen.build()


#def gen_productions(bnf):
    #production_list = bnf_parser.parse(bnf_lexer.lex(bnf))
    #prods = defaultdict(list)
    ## pylint: disable=E1101
    #production_list.visit(prods)
    #return prods
