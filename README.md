# committer [![Build Status](https://secure.travis-ci.org/aelgru/committer.png?branch=master)](http://travis-ci.org/aelgru/committer)


Provides a simplified command line interface to the version control systems git,
mercurial, and subversion.

## Usage

Committer provides three commands: *commit, st,* and *update.*

### Committing all changes in the current directory:

```bash
commit "This is a short message about WHY I made this change."
```
Using the *commit* script on a git repository will:
* check if the "git" command is executable, by executing: *git --version*
* execute: *git pull*
* execute: *git commit -a -m "This is a short message about WHY I made this change."*
* execute: *git push*

### Incrementing the version before committing:

```bash
commit "added a new feature" ++
```

The second argument "++" tells the script to increment the version within
*build.py*


### Show changes in the current directory:

```bash
st
```

This will execute the "status" command known by all version control systems.


### Updating the repository in the current directory:

```bash
update
```

Using the *update* script on a mercurial repository will:
* check if the "hg" command is executable, by executing: *hg --version --quiet*
* execute: *hg pull*
* execute: *hg up*


## Micro Commits

Committing in a high frequency has advantages:
* prevents merging,
* makes code reviews easier, and
* commit messages for smaller commits "tell a story".

[Blog entry by Lucas Rocha: Micro Commits](http://lucasr.org/2011/01/29/micro-commits/)

[Code Ranch Discussion: Macro vs Micro Commits](http://www.coderanch.com/t/106477/vc/Macro-vs-Micro-commits)


## Installation

### Using pip 
```bash
pip install https://github.com/downloads/aelgru/committer/committer-0.0.58.tar.gz
```

### Using easy_install
```
easy_install https://github.com/downloads/aelgru/committer/committer-0.0.58.tar.gz
```


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
