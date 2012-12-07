#   git client for committer
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
    Git command line client wrapper module.
"""

__author__ = 'Michael Gruber'

from os import path

from committer.vcsclients.util import VcsClient


class GitClient(VcsClient):
    
    def __init__(self):
        super(GitClient, self).__init__(name='Git', command='git')

    def commit(self, message):
        """
            commits all files by calling: git commit -a -m "message"
        """
        self._git('commit', '-a', '-m', message)
        self._git('push')
    
    
    def detect(self):
        """
            Checks if the .git directory exists.
            
            @return: True if the current directory represents a git repository,
                     False otherwise.
        """
        return path.isdir('.git')
    
    
    def is_executable(self):
        """
            Checks if "git --version" is executable
             
            @return: True git command line client executable,
                     False otherwise. 
        """
        return self.check_if_is_executable(self.command, '--version')
    
    
    def status(self):
        """
            Shows changes in current directory using "git status".
        """
        self._git('status', '-sb')
    
    
    def update(self):
        """
            Updates files by executing "git pull".
        """
        self._git('pull')
    
    
    def _git(self, *arguments):
        """
            Executes git using the given arguments.
        """
        self.execute_command(self.command, *arguments)
        
git_client = GitClient()
