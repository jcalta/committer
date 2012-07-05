import os
import sys
import subprocess

from committer.git import Git


def increment_version_string (line):
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
    source_file = open('build.py', 'r')
    destination_file = open('build.py.new', 'w')
    
    for line in source_file:
        if line.startswith('version = '):
            line = increment_version_string(line)
        destination_file.write(line)
    
    source_file.close()
    destination_file.close()
    
    os.rename('build.py.new', 'build.py')

def handle_repository (repository, message):
    repository.pull()
    
    increment_version()
    
    repository.commit(message)
    repository.push()
    
def detect_repository ():
    return Git()

def main (arguments):
    repository = detect_repository()
    message = arguments[1]
    handle_repository(repository, message)
