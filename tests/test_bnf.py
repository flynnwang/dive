# -*- coding: utf-8 -*-

import unittest
from collections import defaultdict
from dive.sql.syntax import bnf_lexer, bnf_parser, gen_productions
from dive.sql.syntax.node import OptionalNode


class BNFParserTest(unittest.TestCase):

    def _parse(self, s):
        return bnf_parser.parse(bnf_lexer.lex(s))

    def test_single_production(self):
        bnf = self._parse("main : S;")

        assert bnf[0].ident.value == "main"
        assert bnf[0].alternatives[0][0].value == "S"

    def test_single_prod_with_alternatives(self):
        bnf = self._parse("main : S | E;")
        assert bnf[0].ident.value == "main"
        assert bnf[0].alternatives[0][0].value == "S"
        assert bnf[0].alternatives[1][0].value == "E"

    def test_double_production(self):
        bnf = self._parse("main : A; A : B;")

        assert bnf[0].ident.value == "main"
        assert bnf[0].alternatives[0][0].value == "A"

        assert bnf[1].ident.value == "A"
        assert bnf[1].alternatives[0][0].value == "B"

    def test_optional_items(self):
        bnf = self._parse("main : [A];")

        assert bnf[0].ident.value == "main"
        assert bnf[0].alternatives[0][0].alternatives[0][0].value == "A"

    def test_repetitive_items(self):
        bnf = self._parse("main : {A B};")

        assert bnf[0].ident.value == "main"

        repetitives = bnf[0].alternatives[0][0]
        assert repetitives.alternatives[0][0].value == "A"
        assert repetitives.alternatives[0][1].value == "B"

    #bnf = self._parse("main : {A | B};")


class BNFGenerationTest(unittest.TestCase):

    def _gen(self, s):
        class ClassRepo(dict):

            def __getitem__(self, key):
                if key in self:
                    return super(ClassRepo, self).__getitem__(key)
                return key

        return list(gen_productions(s, ClassRepo()))

    def test_single_prod(self):
        prod = "S : A;"
        prods = self._gen(prod)

        assert 1 == len(prods)
        assert prod == prods[0][0]
        assert "S" == prods[0][1]

    def test_double_prods(self):
        prod = "S : A B;"
        prods = self._gen(prod)

        assert 1 == len(prods)
        assert prod == prods[0][0]
        assert "S" == prods[0][1]

    def test_optional_items(self):
        prod = "S : [A];"
        prods = self._gen(prod)

        assert 3 == len(prods)
        print prods

        assert "S : item_1;" == prods[0][0]
        assert "S" == prods[0][1]

        assert "item_1 : ;" == prods[1][0]
        assert OptionalNode == prods[1][1]

        assert "item_1 : A;" == prods[2][0]
        assert OptionalNode == prods[2][1]

    # TODO: test_repetitive_items
