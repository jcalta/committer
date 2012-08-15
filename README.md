# committer [![Build Status](https://secure.travis-ci.org/aelgru/committer.png?branch=master)](http://travis-ci.org/aelgru/committer)

Unified and simplified command line interface to version control systems.

Supports: Git, Mercurial, and Subversion.


## Usage

* `commit` - commit all changes
* `st` - status: show all changes
* `update` - update the current directory


### Commit all changes:

```bash
commit "This is a short message about WHY I made this change."
```
For example using the `commit` script on a git repository will:
* check if the "git" command is executable, by executing: *git --version*
* execute: *git pull*
* execute: *git commit -a -m "This is a short message about WHY I made this change."*
* execute: *git push*


### Increment the version before committing:

```bash
commit "added a new feature" ++
```

The second argument "++" tells the script to increment the version within
*build.py*


### Show all changes:

```bash
st
```

This will execute the "status" command known by all version control systems.


### Update:

```bash
update
```

For example using the `update` script on a mercurial repository will:
* check if the "hg" command is executable, by executing: *hg --version --quiet*
* execute: *hg pull*
* execute: *hg up*


### Help

```bash
commit help
```
The help argument works on all commands.


### Version Information

```bash
update --version
```
Displays the committer version information. Works on all commands. 


## Installation

### Using pip 
```bash
sudo pip install committer
```

or 

```bash
sudo pip install https://github.com/downloads/aelgru/committer/committer-0.0.58.tar.gz
```

### Using easy_install
```
easy_install https://github.com/downloads/aelgru/committer/committer-0.0.58.tar.gz
```

## Micro Commits

Committing in a high frequency has advantages:
* prevents merging,
* makes code reviews easier, and
* commit messages for smaller commits "tell a story".

[Micro Commits](http://lucasr.org/2011/01/29/micro-commits/)

[Macro vs Micro Commits](http://www.coderanch.com/t/106477/vc/Macro-vs-Micro-commits)


## Alternatives

If you do *not* like the workflow **committer** implies, maybe you are
interested in [hg-git](http://hg-git.github.com/) or [git-svn](http://www.kernel.org/pub/software/scm/git/docs/git-svn.html).

(Thank you very much to [Steve Klabnik](http://www.steveklabnik.com/) for the hint)


## License

Copyright 2012 Michael Gruber

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
