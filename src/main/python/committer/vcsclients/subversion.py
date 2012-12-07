#   subversion client for committer
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
    Subversion command line client wrapper module.
"""

__author__ = 'Michael Gruber'

from os import path

from committer.vcsclients.util import VcsClient


class SubversionClient(VcsClient):
    
    def __init__(self):
        super(SubversionClient, self).__init__(name='Subversion', command='svn')
    
    def commit(self, message):
        """
            Commits all files by calling: svn commit -m "message"
        """
        self._svn('commit', '-m', message)
    
    
    def detect(self):
        """
            Checks if the .svn directory exists.
            
            @return: True if the current directory represents a subversion repository,
                     False otherwise.
        """
        return path.isdir('.svn')
    
    
    def is_executable(self):
        """
            Checks if "svn --version --quiet" is executable.
            
            @return: True if svn client is executable,
                     False otherwise. 
        """
        return self.check_if_is_executable(self.command, '--version', '--quiet')
    
    
    def status(self):
        """
            Shows changes in the current directory using "svn status".
        """
        self._svn('status')
    
    
    def update(self):
        """
            Updates files by executing "svn pull" and "svn update".
        """
        self._svn('update')
    
    
    def _svn(self, *arguments):
        """
            Executes svn using the given arguments.
        """
        self.execute_command(self.command, *arguments)

subversion_client = SubversionClient()