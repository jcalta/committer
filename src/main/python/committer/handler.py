#   handler module for committer
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
    Handling of repositories, offers function commit.
"""

__author__ = 'Michael Gruber'

from committer import incrementor


def commit (repository, message, increment=False):
    """
        performs a pull on the repository. If increment is True it will
        increment the version within build.py and commit using the given
        message. Then it will push the changes. 
    """
    
    repository.update()
    
    if increment:
        incrementor.increment_version()
    
    repository.commit(message)
    
    return 0
