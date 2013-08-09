# -*- coding: utf-8 -*-

import rply
from collections import defaultdict
from node import Node, NodeList, OptionalNode

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
    pass


class Production(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[0], tokens[2])

    def __init__(self, ident, alternatives):
        self.ident = ident
        self.alternatives = alternatives

    def visit(self, ctx):
        name = self.ident.value
        for a in self.alternatives:
            ctx.append(name, a.visit(ctx))


class Alternatives(NodeList):
    pass


class ItemList(NodeList):

    def visit(self, ctx):
        return [it.visit(ctx) for it in self]


class SurroundItems(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[1])

    def __init__(self, alternatives):
        Node.__init__(self)
        self.alternatives = alternatives


class OptionalItems(SurroundItems):

    def visit(self, ctx):
        self.value = ctx.register_cls(OptionalNode)
        ctx.append(self.value, [], OptionalNode)
        for a in self.alternatives:
            ctx.append(self.value, a.visit(ctx), OptionalNode)
        return self.value


class RepetitiveItems(SurroundItems):

    def visit(self, ctx):
        self.value = ctx.register_cls(NodeList)
        ctx.append(self.value, [], NodeList)
        for a in self.alternatives:
            values = a.visit(ctx)
            ctx.append(self.value, values, NodeList)
            ctx.append(self.value, [self.value] + values, NodeList)
        return self.value


class Identifier(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[0])

    def __init__(self, token):
        Node.__init__(self)
        self.token = token

    def visit(self, ctx):
        return self.token.value

    @property
    def value(self):
        return self.token.value
        
        
productions = (
    ('production_list : production', ProductionList),
    ('production_list : production_list production', ProductionList),

    ('production : IDENT COLON alternatives SEMICOLON', Production),

    ('alternatives : item_list', Alternatives),
    ('alternatives : item_list OR item_list', Alternatives),

    ('item_list : item', ItemList),
    ('item_list : item_list item', ItemList),

    ('item : IDENT', Identifier),
    ('item : OPEN_BRACKET alternatives CLOSE_BRACKET', OptionalItems),
    ('item : OPEN_BRACE alternatives CLOSE_BRACE', RepetitiveItems),
)


parser_gen = rply.ParserGenerator(TOKENS.keys(), cache_id="bnf_parser")
for prod, cls in productions:
    parser_gen.production(prod)(cls.production)
bnf_parser = parser_gen.build()


class ProductionGen(object):

    def __init__(self, repo):
        self.repo = repo
        self._prods = []
        self._count = 0

    def register_cls(self, cls):
        self._count += 1
        name = "item_%s" % self._count
        #assert name not in self.repo
        self.repo[name] = cls
        return name

    def append(self, name, values, cls=None):
        if cls is None:
            cls = self.repo[name]
        prod = "%s : %s;" % (name, " ".join(values))
        self._prods.append((prod, cls))

    @property
    def productions(self):
        return reversed(self._prods)


def gen_productions(bnf, repo):
    productions = bnf_parser.parse(bnf_lexer.lex(bnf))
    ctx = ProductionGen(repo)
    # pylint: disable=E1101
    productions.visit(ctx)
    return ctx.productions
