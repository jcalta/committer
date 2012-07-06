import subprocess

def commit (message):
    _git('commit', '-a', '-m', message)

def pull ():
    _git('pull')

def push ():
    _git('push')

def _git (*args):
    arguments = list(args)
    arguments.insert(0, 'git')
    subprocess.call(arguments)

def _ensure_git_is_executable ():
    arguments = ['git', '--version']
    subprocess.check_call(arguments)
