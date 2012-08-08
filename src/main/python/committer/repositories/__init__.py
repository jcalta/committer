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
    Submodules of this module are version control systems command line client 
    wrappers. They are implementing the functions commit, detect, is_executable,
    and update. The module itself provides two functions "find" and "detect".
    The function "find" returns a list of all available repository modules. The
    function detect returns a list of all detected repositories. 
"""

__author__ = 'Michael Gruber'

import sys

from committer import errors
from committer.repositories import git, mercurial, subversion


def detect ():
    """
        returns all detected repository modules. The detection will call detect
        on all found repositories.
    """
    
    repositories = find()
    
    return [repository for repository in repositories if repository.detect()]


def discover_working_repository ():
    """
        returns the detected repository. Will raise an CommitterException when
        no or more than one repository is detected.
    """
    
    detected_repositories = detect()
    
    if len(detected_repositories) == 0:
        raise errors.NoRepositoryDetectedException()
    
    if len(detected_repositories) > 1:
        raise errors.TooManyRepositoriesException(detected_repositories)
    
    repository = detected_repositories[0]
    return ensure_client_executable(repository)


def ensure_client_executable (repository):
    """
        ensures that the command line client for the given repository is
        executable. Will Raise an CommiterException when the command line
        client is not executable.
    """
    
    if not repository.is_executable():
        raise errors.NotExecutableException(repository)
    
    return repository


def find ():
    """
        returns a list of all available version control systems command line
        client wrappper modules (git, mercurial, and subversion).
    """
    
    return [git, mercurial, subversion]
