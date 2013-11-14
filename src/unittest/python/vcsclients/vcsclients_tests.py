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

import unittest
import subprocess

from mockito import mock, when, verify, unstub, never, any as any_value

import committer

from committer.vcsclients import AbstractVcsClient


class AbstractVcsClientTests (unittest.TestCase):
    def setUp(self):
        self.vcs_client = AbstractVcsClient('Name', 'command')

    def tearDown(self):
        unstub()

    def test_should_raise_exception_when_argument_name_not_given(self):
        self.assertRaises(Exception, AbstractVcsClient, None, 'command')

    def test_should_raise_exception_when_argument_command_not_given(self):
        self.assertRaises(Exception, AbstractVcsClient, 'Name', None)

    def test_should_have_property_name(self):
        self.assertEqual('Name', self.vcs_client.name)

    def test_should_have_property_command(self):
        self.assertEqual('command', self.vcs_client.command)

    def test_should_raise_not_implemented_error_when_trying_to_check_if_is_executable(self):
        self.assertRaises(NotImplementedError, self.vcs_client.is_executable)

    def test_should_raise_not_implemented_error_when_trying_to_detect(self):
        self.assertRaises(NotImplementedError, self.vcs_client.detect)

    def test_should_return_true_by_default(self):
        self.assertTrue(self.vcs_client.everything_was_up_to_date)

    def test_should_raise_not_implemented_error_when_trying_to_update(self):
        self.assertRaises(NotImplementedError, self.vcs_client.update)

    def test_should_raise_not_implemented_error_when_trying_to_get_status(self):
        self.assertRaises(NotImplementedError, self.vcs_client.status)

    def test_should_raise_not_implemented_error_when_trying_to_commit(self):
        self.assertRaises(NotImplementedError, self.vcs_client.commit, 'message')
