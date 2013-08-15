# -*- coding: utf-8 -*-

from fabric.api import local


def test(options=""):
    if options:
        options = "-" + options
    local("py.test %s tests/*.py" % options)


def pep8():
    local("find . | grep py$ | xargs autopep8 --in-place")
