committer
=========

[![Build Status](https://secure.travis-ci.org/aelgru/committer.png?branch=master)](http://travis-ci.org/aelgru/committer)

usage:
	commit "message about what you modified" [++]

python script to do the following steps:
* pull
* if second argument is ++ then increment version within build.py
* commit using string in first argument as message
* push
