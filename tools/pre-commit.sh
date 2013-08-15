#!/bin/sh

# cd dive
# ln -s ../../tools/pre-commit.sh .git/hooks/pre-commit

git stash -q --keep-index

py.test -qxvs tests/*.py
RESULT=$?

git stash pop -q

[ $RESULT -ne 0 ] && exit 1
exit 0
