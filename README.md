# committer [![Build Status](https://secure.travis-ci.org/aelgru/committer.png?branch=master)](http://travis-ci.org/aelgru/committer)

Unified command line interface for git, mercurial, and subversion.


## Usage

### Commit all changes

```bash
commit "This is the commit message."
```

Commits all changes in the current directory using the first argument as commit
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
sudo pip install https://github.com/downloads/aelgru/committer/committer-0.0.63.tar.gz
```

### Using easy_install
```
easy_install https://github.com/downloads/aelgru/committer/committer-0.0.63.tar.gz
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


## Micro Commits

Committing in a high frequency has advantages:
* prevents merging,
* makes code reviews easier, and
* commit messages for smaller commits "tell a story".

[Read more about micro commits.](http://lucasr.org/2011/01/29/micro-commits/)


## Alternatives

Did you know all git repositories on GitHub are subversion repositories?

```bash
svn checkout https://github.com/aelgru/committer
```

[Collaborating on GitHub with Subversion](https://github.com/blog/1178-collaborating-on-github-with-subversion)

If you do *not* like the workflow **committer** implies, you may be interested in 
[hg-git](http://hg-git.github.com/) or
[git-svn](http://www.kernel.org/pub/software/scm/git/docs/git-svn.html).

## License

Committer is licensed under the [Apache License, Version 2.0](https://github.com/aelgru/committer/blob/master/LICENSE)
