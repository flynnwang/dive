# -*- coding: utf-8 -*-

import unittest
from collections import defaultdict
from dive.sql.syntax import bnf_lexer, bnf_parser, gen_productions
from dive.sql.syntax.node import OptionalNode, NodeList


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

    def test_empty_item(self):
        bnf = self._parse("S : $;")

        assert bnf[0].ident.value == "S"
        assert bnf[0].alternatives[0][0].value == ""

    def test_triple_items(self):
        bnf = self._parse("S : A | B | C ;")

        assert bnf[0].ident.value == "S"
        assert bnf[0].alternatives[0][0].value == "A"
        assert bnf[0].alternatives[1][0].value == "B"
        assert bnf[0].alternatives[2][0].value == "C"


class BNFGenerationTest(unittest.TestCase):

    def _gen(self, s):
        class ClassRepo(dict):

            def __getitem__(self, key):
                if key in self:
                    return super(ClassRepo, self).__getitem__(key)
                return key

        return list(gen_productions(s, ClassRepo()))

    def test_single_prod(self):
        prods = self._gen("S : A;")

        assert 1 == len(prods)
        assert ("S : A", "S") == prods[0]

    def test_double_prods(self):
        prods = self._gen("S : A B;")

        assert 1 == len(prods)
        assert ("S : A B", "S") == prods[0]

    def test_optional_items(self):
        prods = self._gen("S : [A];")

        assert 3 == len(prods)
        assert ("S : item_1", "S") == prods[0]
        assert ("item_1 : A", OptionalNode) == prods[1]
        assert ("item_1 : ", OptionalNode) == prods[2]

    def test_prod_with_alternatives(self):
        prods = self._gen("S : A | B;")

        assert 2 == len(prods)
        assert ("S : B", "S") == prods[0]
        assert ("S : A", "S") == prods[1]

    def test_select_list(self):
        prod = "select_list : asterisk | select_list comma sublist;"
        prods = self._gen(prod)

        assert 2 == len(prods)
        assert ("select_list : asterisk", "SelectList") == prods[1]
        assert ("select_list : select_list comma sublist",
                "SelectList") == prods[0]
