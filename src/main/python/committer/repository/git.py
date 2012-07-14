#   Copyright 2012, Michael Gruber
#   Licensed under Apache License, Version 2.0

"""
    Git wrapper module.
"""

import subprocess


def commit (message):
    """
        commits all files.
    """
    _git('commit', '-a', '-m', message)

def pull ():
    """
        pulls from repository.
    """
    _git('pull')

def push ():
    """
        pushes to repository.
    """
    _git('push')

def _git (*args):
    """
        executes git using the given arguments.
    """
    arguments = list(args)
    arguments.insert(0, 'git')
    subprocess.call(arguments)

def _ensure_git_is_executable ():
    """
        checks that 'git --version' can be executed,
        will raise an exception if not.
    """
    arguments = ['git', '--version']
    subprocess.check_call(arguments)
