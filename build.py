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
    Build committer using python-builder.
    
    http://code.google.com/p/python-builder
"""

from pythonbuilder.core import Author, init, use_plugin

use_plugin('filter_resources')

use_plugin('python.core')
use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('python.pychecker')
use_plugin('python.pylint')
use_plugin('python.unittest')

authors = [Author('Michael Gruber', 'aelgru@gmail.com')]
license = 'Apache License, Version 2.0'
summary = 'committer - supports iterative and incremental work with repositories.'
url     = 'https://github.com/aelgru/committer'
version = '0.0.37'

default_task = ['analyze', 'publish']

@init
def set_properties (project):
    project.set_property('coverage_break_build', False)
    project.set_property('pychecker_break_build', True)

    project.include_file('committer', 'LICENSE')
    
    project.get_property('filter_resources_glob').append('**/committer/__init__.py')

    project.get_property('distutils_commands').append('bdist_egg')
