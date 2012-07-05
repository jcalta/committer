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
    
    def _git (self, *arguments):
        arguments_list = list(arguments)
        arguments_list.insert(0, 'git')
        subprocess.call(arguments_list)

    def _ensure_git_is_executable (self):
        subprocess.check_call(['git', '--version'])
