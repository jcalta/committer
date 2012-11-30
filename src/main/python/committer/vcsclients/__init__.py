#   version control system clients for committer
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
    Submodules of this module are version control systems clients.
    They are implementing the functions commit, detect, is_executable,
    and update. The module itself provides two functions "find" and "detect".
    The function "find" returns a list of all available vcs client modules. The
    function "discover_working_repository" returns the vcs client for the
    repository in the current directory. 
"""

__author__ = 'Michael Gruber'

from committer import errors
from committer.vcsclients import git, mercurial, subversion


def discover_working_repository ():
    """
        runs vcs_client detection on the current directory.
        
        @raise CommitterException: when no or more than one vcs_client detected.
        @return: the vcs client to the vcs_client in the current directory. 
    """
    
    detected_repositories = _detect_repositories()
    
    if not detected_repositories:
        raise errors.NoRepositoryDetectedError()
    
    if len(detected_repositories) > 1:
        raise errors.TooManyRepositoriesError(detected_repositories)
    
    vcs_client = detected_repositories[0]
    return ensure_executable(vcs_client)


def ensure_executable (vcs_client):
    """
        ensures the given vcs client is executable. 
        
        @raise CommiterException: when the command line client is not executable.
        @return: the given vcs client
    """
    
    if not vcs_client.is_executable():
        raise errors.NotExecutableError(vcs_client)
    
    return vcs_client


def _detect_repositories ():
    """
        runs detection on all available vcs clients. 
        
        @return: list of vcs clients
    """
    
    vcs_clients = _find()
    
    return [vcs_client for vcs_client in vcs_clients if vcs_client.detect()]


def _find ():
    """
        @return: list of all available vcs client modules.
    """
    
    return [git, mercurial, subversion]
