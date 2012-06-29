import subprocess


class Git (object):
    def __init__ (self):
        self._is_executable()
        
    def call_git (self, *arguments):
        arguments_list = list(arguments)
        arguments_list.insert(0, 'git')
        subprocess.call(arguments_list)

    def commit (self, message):
        self.call_git('commit', '-a', '-m', message)
    
    def pull (self):
        self.call_git('pull')
    
    def push (self):
        self.call_git('push')
    
    def _is_executable (self):
        subprocess.check_call(['git', '--version'])
