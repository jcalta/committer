#   mercurial client for committer
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
    Mercurial command line client wrapper module.
"""

__author__ = 'Michael Gruber'

from os import path

from committer.vcsclients.util import VcsClient

COMMAND = 'hg'
NAME = 'Mercurial'

class MercurialClient(VcsClient):
    def commit(self, message):
        """
            Commits all files in the current directory by calling: 
                hg commit -m "message"
                hg push
        """
        self._hg('commit', '-m', message)
        self._hg('push')
    
    
    def detect(self):
        """
            Checks if the .hg directory exists.
            
            @return: True if the current directory represents a mercurial repository,
                     False otherwise.
        """
        return path.isdir('.hg')
    
    
    def is_executable(self):
        """
            @return: True if "hg --version --quiet" is executable,
                     False otherwise. 
        """
        return self.check_if_is_executable(COMMAND, '--version', '--quiet')
    
    
    def status(self):
        """
            Shows changes in the current directory using "hg status".
        """
        self._hg('status')
    
    
    def update(self):
        """
            Updates files by calling "hg pull" and "hg update".
        """
        self._hg('pull')
        self._hg('update')
    
    
    def _hg(self, *arguments):
        """
            Executes hg using the given arguments.
        """
        self.execute_command(COMMAND, *arguments)

mercurial_client = MercurialClient()