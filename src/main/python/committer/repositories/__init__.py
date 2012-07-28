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
    Submodules of this module are vcs command line client wrappers. They are
    implementing the functions commit, detect, is_executable, and update. The
    module itself provides two functions 'find' and 'detect'. The function
    'find' returns a list of all available repository modules. The function
    detect returns a list of all deteceted repositories. 
"""

__author__ = 'Michael Gruber'

import sys

from committer.repositories import git, mercurial, subversion


def detect ():
    """
        returns all detected repository modules. The detection will call detect
        on all found repositories.
    """
    
    detected_repositories = []
    list_of_repositories  = find()
    
    for repository in list_of_repositories:
        if repository.detect():
            detected_repositories.append(repository)
    
    return detected_repositories


def find ():
    """
        returns a list of all available vcs command line wrappper modules.
    """
    
    return [git, mercurial, subversion]

