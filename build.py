#   committer
#   Copyright 2012-2013 Michael Gruber
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
    Build committer using pybuilder.

    https://github.com/pybuilder/pybuilder
"""

from pybuilder.core import Author, init, use_plugin

use_plugin('python.core')

use_plugin('copy_resources')
use_plugin('filter_resources')

use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('python.flake8')
use_plugin('python.install_dependencies')
use_plugin('python.unittest')

url = 'https://github.com/aelgru/committer'
description = 'Please visit {0} for more information!'.format(url)

authors = [Author('Michael Gruber', 'aelgru@gmail.com')]
license = 'Apache License, Version 2.0'
summary = 'Unified command line interface for git, mercurial, and subversion.'
version = '0.1.4'

default_task = ['analyze', 'publish']

@init
def set_properties (project):
    project.build_depends_on('coverage')
    project.build_depends_on('mock')
    project.build_depends_on('mockito')

    project.set_property('coverage_break_build', True)

    project.set_property('copy_resources_target', '$dir_dist/committer')
    project.get_property('copy_resources_glob').append('LICENSE')

    project.include_file('committer', 'LICENSE')

    project.get_property('filter_resources_glob').append('**/committer/__init__.py')

    project.set_property('flake8_verbose_output', True)
    project.set_property('flake8_break_build', True)

    project.get_property('distutils_commands').append('bdist_egg')
    project.set_property('distutils_classifiers', [
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Version Control',
          'Topic :: Utilities'])
