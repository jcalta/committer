# _committer_

Unified command line interface for *git*, *mercurial* and *subversion*.

```
Usage:
    ci "message"     commits all changes
    st               shows all changes
    up               updates the current directory

Options:
    -h --help        show this help screen
    --debug          enable logging of debug messages
    --version        show version information
```

_committer_ is best used in combination with [ssh keys](https://help.github.com/articles/generating-ssh-keys) or [credential-cache](http://git-scm.com/docs/git-credential-cache).

[![Build Status](https://secure.travis-ci.org/aelgru/committer.png?branch=master)](http://travis-ci.org/aelgru/committer)
[![Coverage](https://coveralls.io/repos/aelgru/committer/badge.png?branch=master)](https://coveralls.io/r/aelgru/committer)
[![PyPI version](https://badge.fury.io/py/committer.png)](http://badge.fury.io/py/committer)
[![Downloads](https://pypip.in/d/committer/badge.png)](https://pypi.python.org/pypi/committer)
[![License](https://pypip.in/license/committer/badge.png)](https://raw.github.com/aelgru/committer/master/src/main/python/committer/LICENSE.txt)

## How to Install

```bash
sudo pip install committer
```

[More ways to install committer](https://github.com/aelgru/committer/blob/master/INSTALL.md)

## Features

### Commit

How many times did you forget to update before committing your changes?

```bash
ci "This is the commit message."
```

Updates the repository in the current working directory.
Only commits your changes when no update-changes have been found.

### Status

```bash
st
```

Executes the "status" command known by all version control systems.


### Update

```bash
up
```

Updates the current working directory.

## Configuration

It is possible to force committer to execute a command (with arguments)
before performing any other action. Put a INI file called `.committerrc` in your current
working directory. Example configuration to execute flake8:

```
[DEFAULT]
execute_before = flake8
```

If you want to execute a command only before commit please create a section called commit like this:
```
[COMMIT]
execute_before = pyb -v
```

Another good example of the usage of this is to pull from upstream master when you are working in a fork
```
[COMMIT]
execute_before = git pull upstream master
```

[See `.committerrc` in the committer repository.](https://github.com/aelgru/committer/blob/master/.committerrc)

## Micro Commits

Committing in a high frequency has advantages:
* prevents merging,
* makes code reviews easier, and
* commit messages for smaller commits "tell a story".

Read more on best practices:
* [Micro commits](http://lucasr.org/2011/01/29/micro-commits/)
* [A note about git commit messages](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
* [Should I use past or present tense in git commit messages?](http://stackoverflow.com/questions/3580013/should-i-use-past-or-present-tense-in-git-commit-messages)

## How to Contribute

[Read how to build committer yourself](https://github.com/aelgru/committer/blob/master/HOWTO.md)

## Alternatives

Did you know all Git repositories on GitHub can be handled using a subversion client?

```bash
svn checkout https://github.com/aelgru/committer
```

[Collaborating on GitHub with Subversion](https://github.com/blog/1178-collaborating-on-github-with-subversion)

If you do *not* like the workflow **committer** implies, you may be interested in
[hg-git](http://hg-git.github.com/) or
[git-svn](http://www.kernel.org/pub/software/scm/git/docs/git-svn.html).
