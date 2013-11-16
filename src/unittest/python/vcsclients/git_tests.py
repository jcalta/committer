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

from mockito import when, verify, any as any_value, unstub
from committer.vcsclients.git import GitClient

import committer


class GitClientTests(unittest.TestCase):
    def setUp(self):
        self.git_client = GitClient()

    def tearDown(self):
        unstub()

    def test_should_have_command_property(self):
        self.assertEqual('git', self.git_client.command)

    def test_should_have_name_property(self):
        self.assertEqual('Git', self.git_client.name)

    def test_should_prepend_git_to_given_arguments(self):
        when(self.git_client)._git(any_value()).thenReturn(None)

        self.git_client.commit('This is a commit message.')

        verify(self.git_client)._git('commit', '-a', '-m', 'This is a commit message.')
        verify(self.git_client)._git('push')

    def test_should_call_pull(self):
        when(self.git_client)._git(any_value()).thenReturn(None)

        self.git_client.update()

        verify(self.git_client)._git('pull')

    def test_should_save_result(self):
        update_result = {'stdout': 'abc', 'stderr': 'err', 'returncode': 123}
        when(self.git_client)._git(any_value()).thenReturn(update_result)

        self.git_client.update()

        verify(self.git_client)._git('pull')
        self.assertEqual(update_result, self.git_client._update_result)

    def test_should_call_status(self):
        when(self.git_client)._git(any_value()).thenReturn(None)

        self.git_client.status()

        verify(self.git_client)._git('status', '-sb')

    def test_return_false_if_dot_git_directory_does_not_exist(self):
        when(committer.vcsclients.git.path).isdir(any_value()).thenReturn(False)

        actual_return_value = self.git_client.detect()

        self.assertEqual(False, actual_return_value)
        verify(committer.vcsclients.git.path).isdir('.git')

    def test_return_true_if_dot_git_directory_exists(self):
        when(committer.vcsclients.git.path).isdir(any_value()).thenReturn(True)

        actual_return_value = self.git_client.detect()

        self.assertEqual(True, actual_return_value)
        verify(committer.vcsclients.git.path).isdir('.git')

    def test_should_return_value_of_check(self):
        when(committer.vcsclients.git).check_if_is_executable(any_value(), any_value()).thenReturn('value from check')

        actual_return_value = self.git_client.is_executable()

        self.assertEqual('value from check', actual_return_value)
        verify(committer.vcsclients.git).check_if_is_executable('git', '--version')

    def test_should_execute_git_using_arguments(self):
        when(committer.vcsclients.git).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn(None)

        self.git_client._git('arg1', 'arg2', 'arg3')

        verify(committer.vcsclients.git).execute_command('git', 'arg1', 'arg2', 'arg3')

    def test_should_return_stdout_and_stderr_from_execution(self):
        stdout = 'stdout'
        stderr = 'stderr'
        when(committer.vcsclients.git).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn((stdout, stderr))

        actual_stdout, actual_stderr = self.git_client._git('arg1', 'arg2', 'arg3')

        self.assertEqual(stdout, actual_stdout)
        self.assertEqual(stderr, actual_stderr)
    
    def test_should_return_false_if_last_update_found_updates(self):
        self.git_client._update_result = {'stdout': 'Found updates ... blabla'}
        
        actual = self.git_client.everything_was_up_to_date
        
        self.assertFalse(actual)
        
    def test_should_return_true_if_everything_is_up_to_date(self):
        self.git_client._update_result = {'stdout': 'Already up-to-date.\n'}

        actual = self.git_client.everything_was_up_to_date
        
        self.assertTrue(actual)
