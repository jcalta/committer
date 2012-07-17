#   Copyright 2012, Michael Gruber
#   Licensed under Apache License, Version 2.0

"""
    Committer main module.
"""

import os
import sys
import subprocess

from committer.repository import git


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

def handle_repository (repository, message, increment=False):
    """
        performs a pull on the repository. If increment is True it will
        increment the version within build.py and commit using the given
        message. Then it will push the changes. 
    """
    
    repository.pull()
    
    if increment:
        increment_version()
    
    repository.commit(message)
    repository.push()
    
def detect_repository ():
    """
        since detection does not work right now,
        this will simply return a git repository.
    """
    
    return git

def main (arguments):
    """
        will exit with 1 when no arguments are given.
        will use first argument as commit message.
        will increment if second argument is ++
    """
    
    if len(arguments) == 0:
        sys.stdout.write('usage: commit "message" [++]') 
        return sys.exit(1)
    
    repository = detect_repository()
    
    message = arguments[1]
    if len(arguments) == 3 and arguments[2] == '++':
        handle_repository(repository, message, increment=True)
        return
        
    handle_repository(repository, message)
