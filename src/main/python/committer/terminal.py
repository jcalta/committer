#   committer terminal printing
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
    This module provides functions to print to the terminal.
"""

__author__ = 'Michael Gruber'


import sys


def print_text(text):
    sys.stdout.write(text)


def print_error(error_text):
    sys.stderr.write(error_text)
