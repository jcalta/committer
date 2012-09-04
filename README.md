# committer [![Build Status](https://secure.travis-ci.org/aelgru/committer.png?branch=master)](http://travis-ci.org/aelgru/committer)

Unified command line interface for version control systems.

Supports: Git, Mercurial, and Subversion.


## Usage

* `commit` - commit all changes
* `st` - status: show all changes
* `update` - update the current directory


### Commit all changes

```bash
commit "This is the commit message."
```

Commits all changes in the current directory using the given string as commit
message.


### Show all changes

```bash
st
```

Executes the "status" command known by all version control systems.


### Update the current directory

```bash
update
```

## Installation

### Using pip 
```bash
sudo pip install committer
```

or 

```bash
sudo pip install https://github.com/downloads/aelgru/committer/committer-0.0.60.tar.gz
```

### Using easy_install
```
easy_install https://github.com/downloads/aelgru/committer/committer-0.0.60.tar.gz
```

## How does it work?

*Example 1:* performing `commit` on a git repository will:
* check if the `git` command is executable, by executing `git --version`
* execute `git pull`
* execute `git commit -a -m "Extracted interface."`
* execute `git push`


*Example 2:* performing `update` on a mercurial repository will:
* check if the `hg` command is executable, by executing: `hg --version --quiet`
* execute `hg pull`
* execute `hg up`

## Additional Features

### Increment the version before committing

```bash
commit "Added new feature" ++
```

The second argument "++" tells the script to increment the version within
*build.py*


## Micro Commits

Committing in a high frequency has advantages:
* prevents merging,
* makes code reviews easier, and
* commit messages for smaller commits "tell a story".

[Micro Commits](http://lucasr.org/2011/01/29/micro-commits/)

[Macro vs Micro Commits](http://www.coderanch.com/t/106477/vc/Macro-vs-Micro-commits)


## Alternatives

If you do *not* like the workflow **committer** implies, you may be interested in 
[hg-git](http://hg-git.github.com/) or
[git-svn](http://www.kernel.org/pub/software/scm/git/docs/git-svn.html).


## License

Copyright 2012 Michael Gruber
Committer is licensed under the Apache License, Version 2.0
