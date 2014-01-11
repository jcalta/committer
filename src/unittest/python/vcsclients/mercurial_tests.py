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

from fluentmock import ANY_ARGUMENTS, UnitTests, when, verify

from committer.vcsclients import mercurial


class MercurialClientTests(UnitTests):

    def set_up(self):
        self.mercurial_client = mercurial.MercurialClient()

    def test_should_have_command_property(self):
        self.assertEqual('hg', self.mercurial_client.command)

    def test_should_have_name_property(self):
        self.assertEqual('Mercurial', self.mercurial_client.name)

    def test_should_prepend_hg_to_given_arguments(self):
        when(self.mercurial_client)._hg(ANY_ARGUMENTS).then_return(None)
        when(self.mercurial_client)._hg(ANY_ARGUMENTS).then_return(None)

        self.mercurial_client.commit('This is a commit message.')

        verify(self.mercurial_client)._hg('commit', '-m', 'This is a commit message.')
        verify(self.mercurial_client)._hg('push')

    def test_should_call_pull_and_update(self):
        when(self.mercurial_client)._hg(ANY_ARGUMENTS).then_return(None)

        self.mercurial_client.update()

        verify(self.mercurial_client)._hg('pull')
        verify(self.mercurial_client)._hg('update')

    def test_should_store_update_result(self):
        when(self.mercurial_client)._hg('update').then_return('update result')

        self.mercurial_client.update()

        self.assertEqual('update result', self.mercurial_client._update_result)

    def test_should_call_status(self):
        when(self.mercurial_client)._hg(ANY_ARGUMENTS).then_return(None)

        self.mercurial_client.status()

        verify(self.mercurial_client)._hg('status')

    def test_return_false_if_dot_hg_directory_does_not_exist(self):
        when(mercurial.path).isdir(ANY_ARGUMENTS).then_return(False)

        actual_return_value = self.mercurial_client.detect()

        self.assertEqual(False, actual_return_value)
        when(mercurial.path).isdir('.hg')

    def test_return_true_if_dot_hg_directory_exists(self):
        when(mercurial.path).isdir(ANY_ARGUMENTS).then_return(True)

        actual_return_value = self.mercurial_client.detect()

        self.assertEqual(True, actual_return_value)
        when(mercurial.path).isdir('.hg')

    def test_should_return_value_of_check(self):
        when(mercurial).check_if_is_executable(ANY_ARGUMENTS).then_return('value from check')

        actual_return_value = self.mercurial_client.is_executable()

        self.assertEqual('value from check', actual_return_value)
        verify(mercurial).check_if_is_executable('hg', '--version', '--quiet')

    def test_should_execute_hg_using_arguments(self):
        when(mercurial).execute_command(ANY_ARGUMENTS).then_return(None)

        self.mercurial_client._hg('arg1', 'arg2', 'arg3')

        verify(mercurial).execute_command('hg', 'arg1', 'arg2', 'arg3')

    def test_should_return_execution_result(self):
        when(mercurial).execute_command(ANY_ARGUMENTS).then_return({'stdout': 'abc', 'stderr': 'err', 'returncode': 123})

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
