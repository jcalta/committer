# committer

Unified command line interface for *git*, *mercurial*, and *subversion*.

## How to Install

```bash
sudo pip install committer
```
[More ways to install committer](https://github.com/aelgru/committer/blob/master/INSTALL.md)

## How to Commit

### How many times did you forget to update before committing your changes?

```bash
ci "This is the commit message."
```

Updates the repository in the current working directory.
Then commits all changes using the first argument as commit message.


### Show all changes

```bash
st
```

Executes the "status" command known by all version control systems.


### Update the current directory

```bash
up
```

### Micro Commits

Committing in a high frequency has advantages:
* prevents merging,
* makes code reviews easier, and
* commit messages for smaller commits "tell a story".

[Read more about micro commits.](http://lucasr.org/2011/01/29/micro-commits/)
## How to Contribute

Simply [fork](https://github.com/aelgru/committer/fork_select) committer.

[Read how to build committer yourself](https://github.com/aelgru/committer/blob/master/HOWTO.md)

[![Build Status](https://secure.travis-ci.org/aelgru/committer.png?branch=master)](http://travis-ci.org/aelgru/committer)

## Alternatives

Did you know all Git repositories on GitHub can be handled using a subversion client?

```bash
svn checkout https://github.com/aelgru/committer
```

[Collaborating on GitHub with Subversion](https://github.com/blog/1178-collaborating-on-github-with-subversion)

If you do *not* like the workflow **committer** implies, you may be interested in 
[hg-git](http://hg-git.github.com/) or
[git-svn](http://www.kernel.org/pub/software/scm/git/docs/git-svn.html).

## License

Committer is licensed under the [Apache License, Version 2.0](https://github.com/aelgru/committer/blob/master/LICENSE)
