# -*- coding: utf-8 -*-

import os
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


def testone(case="SelectWhereTest", opt="qxv"):
    if opt:
        opt = "-" + opt
    local("py.test %s tests/*.py -k %s" % (opt, case))


def pep8():
    local("find . | grep py$ | xargs autopep8 --in-place")


def setup_dev_env():
    if not os.path.exists('bin'):
        os.mkdir('bin')
    local("virtualenv --system-site-packages bin/env")
    local("pip install -r requirements.txt")
