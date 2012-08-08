#   committer errors and exceptions
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
    Contains exceptions.
"""

__author__ = 'Michael Gruber'


class CommitterException (Exception):
    """
        to be raised when an error occurred, which should stop the default
        program flow.
    """
    
    def __init__ (self, message, error_code):
        """
            will set the given properties.
        """
        if error_code == 0:
            raise Exception('Illegal error code "zero".')

        if error_code > 127:
            raise Exception(
                      'Illegal error code "%s": has to be smaller than 128.',
                      error_code)
        
        super(CommitterException, self).__init__()
        self.message    = message + '\n'
        self.error_code = error_code


class NoRepositoryDetectedException (CommitterException):
    """
        to be raised when no repository could be detected in the current
        directory.
    """
    
    def __init__ (self):
        super(NoRepositoryDetectedException, self) \
            .__init__('No repository detected.', 100)

class ShowUsageInformationException (CommitterException):
    """
        to be raised when showing the usage information.
    """

    def __init__ (self, usage_information):
        super(ShowUsageInformationException, self) \
            .__init__(usage_information, 1)
    
    
class TooManyRepositoriesException (CommitterException):
    """
        to be raised when more than one repository could be detected in the
        current directory.
    """
    
    def __init__ (self, detected_repositories):
        names = [repository.NAME for repository in detected_repositories] 
        message = 'Detected more than one repository: ' \
                + ', '.join(names)
            
        super(TooManyRepositoriesException, self) \
            .__init__(message, 101)


class NotExecutableException (CommitterException):
    """
        to be raised when the command line client of the repository could not
        be executed.
    """
    
    def __init__ (self, repository):
        super_class = super(NotExecutableException, self)
        message = ('%s command line client "%s" not executable.' 
                   % (repository.NAME, repository.COMMAND)) 
        super_class.__init__(message, 102)
