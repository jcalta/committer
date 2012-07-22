#   incrementor module for committer
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
    Increments version within build.py for python-builder.
"""

__author__ = 'Michael Gruber'

import os

def increment_version_string (line):
    """
        retrieves the version from line and increments 
        the last number within the version.
    """
    
    start_of_version = line.find('\'') + 1
    end_of_version = line.rfind('\'')
    version = line[start_of_version:end_of_version]
    start_of_subversion = version.rfind('.') + 1
    subversion = int(version[start_of_subversion:])
    subversion += 1
    new_version = version[:start_of_subversion] + str(subversion)
    print "version: %s -> %s" % (version, new_version)
    line = line[0:start_of_version] + new_version + line[end_of_version:]
    return line

def increment_version ():
    """
        opens build.py and increments the last number
        of the version.
    """
    
    source_file = open('build.py', 'r')
    destination_file = open('build.py.new', 'w')
    
    for line in source_file:
        if line.startswith('version = '):
            line = increment_version_string(line)
        destination_file.write(line)
    
    source_file.close()
    destination_file.close()
    
    os.rename('build.py.new', 'build.py')
