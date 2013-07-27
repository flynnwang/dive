#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import local


def test_lexer():
    local("py.test -sv tests.py -k LexerTest")


def test_parser():
    local("py.test -sv tests.py -k SqlParserText")


def tests():
    local("py.test -v tests.py")


def run_pep8():
    local("find . | grep py$ | xargs autopep8 --in-place")
