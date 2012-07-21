#   repository module for committer
#   Copyright 2012 Michael Gruber
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
    Submodules of this module are repository wrappers. They are implementing
    the functions pull, commit, push and detect.    
"""

import sys

from committer.repositories import git


DEFAULT = [git]


def detect ():
    """
        detection will return the git repository right now.
    """
    
    if git.detect():
        print 'Detected git repository.'
        return git
    
    sys.exit(1)