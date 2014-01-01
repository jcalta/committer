#   committer
#   Copyright 2012-2014 Michael Gruber
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

from mockito import when, verify, unstub, any as any_value

from committer.vcsclients.mercurial import MercurialClient
import committer


class MercurialClientTests(unittest.TestCase):

    def setUp(self):
        self.mercurial_client = MercurialClient()

    def tearDown(self):
        unstub()

    def test_should_have_command_property(self):
        self.assertEqual('hg', self.mercurial_client.command)

    def test_should_have_name_property(self):
        self.assertEqual('Mercurial', self.mercurial_client.name)

    def test_should_prepend_hg_to_given_arguments(self):
        when(self.mercurial_client)._hg(any_value(), any_value(), any_value()).thenReturn(None)
        when(self.mercurial_client)._hg(any_value()).thenReturn(None)

        self.mercurial_client.commit('This is a commit message.')

        verify(self.mercurial_client)._hg('commit', '-m', 'This is a commit message.')
        verify(self.mercurial_client)._hg('push')

    def test_should_call_pull_and_update(self):
        when(self.mercurial_client)._hg(any_value()).thenReturn(None)

        self.mercurial_client.update()

        verify(self.mercurial_client)._hg('pull')
        verify(self.mercurial_client)._hg('update')

    def test_should_store_update_result(self):
        when(self.mercurial_client)._hg(any_value()).thenReturn(None)
        when(self.mercurial_client)._hg('update').thenReturn('update result')

        self.mercurial_client.update()

        self.assertEqual('update result', self.mercurial_client._update_result)

    def test_should_call_status(self):
        when(self.mercurial_client)._hg(any_value()).thenReturn(None)

        self.mercurial_client.status()

        verify(self.mercurial_client)._hg('status')

    def test_return_false_if_dot_hg_directory_does_not_exist(self):
        when(committer.vcsclients.mercurial.path).isdir(any_value()).thenReturn(False)

        actual_return_value = self.mercurial_client.detect()

        self.assertEqual(False, actual_return_value)
        when(committer.vcsclients.mercurial.path).isdir('.hg')

    def test_return_true_if_dot_hg_directory_exists(self):
        when(committer.vcsclients.mercurial.path).isdir(any_value()).thenReturn(True)

        actual_return_value = self.mercurial_client.detect()

        self.assertEqual(True, actual_return_value)
        when(committer.vcsclients.mercurial.path).isdir('.hg')

    def test_should_return_value_of_check(self):
        when(committer.vcsclients.mercurial).check_if_is_executable(any_value(), any_value(), any_value()).thenReturn('value from check')

        actual_return_value = self.mercurial_client.is_executable()

        self.assertEqual('value from check', actual_return_value)
        verify(committer.vcsclients.mercurial).check_if_is_executable('hg', '--version', '--quiet')

    def test_should_execute_hg_using_arguments(self):
        when(committer.vcsclients.mercurial).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn(None)

        self.mercurial_client._hg('arg1', 'arg2', 'arg3')

        verify(committer.vcsclients.mercurial).execute_command('hg', 'arg1', 'arg2', 'arg3')

    def test_should_return_execution_result(self):
        when(committer.vcsclients.mercurial).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn({'stdout': 'abc', 'stderr': 'err', 'returncode': 123})

        actual_result = self.mercurial_client._hg('arg1', 'arg2', 'arg3')

        self.assertEqual({'stdout': 'abc', 'stderr': 'err', 'returncode': 123}, actual_result)

    def test_should_return_false_if_last_update_found_updates(self):
        self.mercurial_client._update_result = {'stdout': 'Found updates ... blabla'}

        actual = self.mercurial_client.everything_was_up_to_date

        self.assertFalse(actual)

    def test_should_return_true_if_everything_is_up_to_date(self):
        self.mercurial_client._update_result = {'stdout': """resolving manifests
0 files updated, 0 files merged, 0 files removed, 0 files unresolved\n"""}

        actual = self.mercurial_client.everything_was_up_to_date

        self.assertTrue(actual)
