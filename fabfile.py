# -*- coding: utf-8 -*-

from fabric.api import local


def test(opt="qsx"):
    """ run all tests 
        -q  quite
        -s  no capture
        -x  stop when fail
    """
    if opt:
        opt = "-" + opt
    local("py.test %s tests/*.py" % opt)


def pep8():
    local("find . | grep py$ | xargs autopep8 --in-place")
