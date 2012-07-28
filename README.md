committer [![Build Status](https://secure.travis-ci.org/aelgru/committer.png?branch=master)](http://travis-ci.org/aelgru/committer)
=========

Provides a simplified command line interface to the version control systems git,
mercurial, and subversion. 

```bash
commit "This is a short message about WHY I made this change."
```
If you use the *commit* script on a git repository this will:
* check if the 'git' command is executable, by executing 'git --version'
* execute 'git pull'
* execute 'git commit -a -m "This is a short message about WHY I made this change."'
* execute 'git push'

*Incrementing versions before committing*

```bash
commit "added a new feature" ++
```

The second argument '++' will tell the script to increment the version within
*build.py*


*Updating the repository in the current directory* 

```bash
update
```

If you are using the 'update' script on a mercurial repository this will:
* check if the 'hg' command is executable, by executing 'hg --version --quiet'
* execute 'hg pull'
* execute 'hg up'

Micro Commits
=============

Committing more often has benefits:
http://lucasr.org/2011/01/29/micro-commits/


License
=======

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
