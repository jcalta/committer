#   Copyright 2012, Michael Gruber
#   Licensed under Apache License, Version 2.0

from pythonbuilder.core import Author, init, use_plugin

use_plugin('python.core')
use_plugin('python.coverage')
use_plugin('python.unittest')
use_plugin('python.integrationtest')
use_plugin('python.distutils')
use_plugin('python.pychecker')
use_plugin('python.pydev')
use_plugin('python.pylint')

authors = [Author('Michael Gruber', 'aelgru@gmail.com')]
license = 'Apache License, Version 2.0'
summary = 'committer - supports iterative and incremental work with repositories.'
url     = 'https://github.com/aelgru/committer'
version = '0.0.15'

default_task = ['analyze', 'run_integration_tests']

@init
def set_properties (project):
    project.set_property('coverage_break_build', False)
    
    project.set_property('pychecker_break_build', True)
    project.set_property('pychecker_args', ['-Q', '-b', 'unittest'])
