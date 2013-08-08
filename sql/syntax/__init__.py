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
        ctx.name = self.ident.value
        self.alternatives.visit(ctx)


class Alternatives(NodeList):

    def visit(self, ctx):
        name = ctx.name
        for a in self:
            values = a.visit(ctx)
            ctx.append(name, values)


class ItemList(NodeList):

    def visit(self, ctx):
        # assume all Identifiers
        values = []
        for it in self:
            it.visit(ctx)
            values.append(it.value)
        return values


class SurroundItems(Node):

    @classmethod
    def parse(cls, tokens):
        return cls(tokens[1])

    def __init__(self, alternatives):
        Node.__init__(self)
        self.alternatives = alternatives


class OptionalItems(SurroundItems):

    @property
    def value(self):
        return self.name

    def visit(self, ctx):
        name = ctx.register_cls(OptionalNode)

        ctx.name = name
        self.alternatives.visit(ctx)
        ctx.append(name, [], OptionalNode)

        self.name = name


class RepetitiveItems(SurroundItems):

    @property
    def value(self):
        return self.name

    def visit(self, ctx):
        self.name = ctx.register_cls(OptionalItems)


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

    def visit(self, ctx):
        pass
        
        
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
