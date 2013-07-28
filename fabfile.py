#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import local


def test():
    local("py.test -v tests/*.py")


def run_pep8():
    local("find . | grep py$ | xargs autopep8 --in-place")
