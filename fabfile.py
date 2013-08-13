# -*- coding: utf-8 -*-

from fabric.api import local


def test(options=""):
    local("py.test -%sqx tests/*.py" % options)


def pep8():
    local("find . | grep py$ | xargs autopep8 --in-place")
