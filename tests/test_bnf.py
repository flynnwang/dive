# -*- coding: utf-8 -*-

import unittest
from dive.sql.syntax import bnf_lexer, bnf_parser


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
        assert bnf[0].alternatives[0][0].item_list[0].value == "A"

    def test_repetitive_items(self):
        bnf = self._parse("main : {A B};")

        assert bnf[0].ident.value == "main"

        repetitives = bnf[0].alternatives[0][0]
        assert repetitives.item_list[0].value == "A"
        assert repetitives.item_list[1].value == "B"

    def test_empty_prod(self):
        bnf = self._parse("main : ;")

        assert bnf[0].ident.value == "main"
        assert len(bnf[0].alternatives[0]) == 0



