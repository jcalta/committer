from pythonbuilder.core import use_plugin, init, Author

use_plugin('python.core')
use_plugin('python.coverage')
use_plugin('python.unittest')
use_plugin('python.integrationtest')
use_plugin('python.distutils')
use_plugin('python.pychecker')
use_plugin('python.pydev')
use_plugin('python.pylint')

default_task = ['analyze', 'run_integration_tests']

version = '0.0.6'
summary = 'commit - git pull, increase version number in build.py, git commit, git push'
authors = [
    Author('Michael Gruber', 'aelgru@gmail.com'),
]

url = 'https://github.com/aelgru/commit'
license = 'GNU GPL v3'

@init
def set_properties (project):
    project.set_property('coverage_break_build', True)
    project.set_property('pychecker_break_build', True)
    project.set_property('pychecker_args', ['-Q', '-b', 'unittest'])
