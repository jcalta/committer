import subprocess


class Git (object):
    def __init__ (self):
        self._ensure_git_is_executable()
        
    def commit (self, message):
        self._git('commit', '-a', '-m', message)
    
    def pull (self):
        self._git('pull')
    
    def push (self):
        self._git('push')
    
    def _git (self, *args):
        arguments = list(args)
        arguments.insert(0, 'git')
        subprocess.call(arguments)

    def _ensure_git_is_executable (self):
        arguments = ['git', '--version']
        subprocess.check_call(arguments)
