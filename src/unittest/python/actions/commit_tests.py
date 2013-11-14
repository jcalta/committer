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

from mock import call, patch

import unittest_support

from committer.actions import commit
from committer.errors import WrongUsageError


class CommitTests (unittest_support.TestCase):
    def test_should_show_usage_information_when_exactly_one_argument(self):
        self.assertRaises(WrongUsageError, commit, ['/usr/local/bin/commit'])

    @patch('committer.actions.detect_vcs_client')
    def test_should_detect_vcs_client(self, mock_detect):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_detect.return_value = mock_vcs_client

        commit(['/usr/local/bin/commit', 'This is the message'])

        self.assertEqual(call(), mock_detect.call_args)

    @patch('committer.actions.detect_vcs_client')
    def test_should_update_before_committing (self, mock_detect):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_detect.return_value = mock_vcs_client

        commit(['/usr/local/bin/commit', 'This is the message'])

        self.assertEqual(call(), mock_vcs_client.update.call_args)

    @patch('committer.actions.exit')
    @patch('committer.actions.LOGGER')
    @patch('committer.actions.detect_vcs_client')
    def test_should_not_commit_when_update_found_changes(self, mock_discover, mock_logger, mock_exit):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.everything_was_up_to_date = False
        mock_discover.return_value = mock_vcs_client

        commit(['/usr/local/bin/commit', 'This is the message'])

        self.assertEqual(None, mock_vcs_client.commit.call_args)

    @patch('committer.actions.LOGGER')
    @patch('committer.actions.detect_vcs_client')
    def test_should_commit_when_no_changes_found(self, mock_discover, mock_logger):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.everything_was_up_to_date = True
        mock_discover.return_value = mock_vcs_client

        commit(['/usr/local/bin/commit', 'This is the message'])

        self.assertEqual(call('This is the message'), mock_vcs_client.commit.call_args)

    @patch('committer.actions.exit')
    @patch('committer.actions.LOGGER')
    @patch('committer.actions.detect_vcs_client')
    def test_should_print_error_message_when_found_changes(self, mock_discover, mock_logger, mock_exit):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.everything_was_up_to_date = False
        mock_discover.return_value = mock_vcs_client

        commit(['/usr/local/bin/commit', 'This is the message'])

        self.assertEqual(call('Commit interrupted: unexpected "update" result or "update" found changes.'), mock_logger.error.call_args)

    @patch('committer.actions.exit')
    @patch('committer.actions.LOGGER')
    @patch('committer.actions.detect_vcs_client')
    def test_should_exit_with_error_when_found_changes(self, mock_discover, mock_logger, mock_exit):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.everything_was_up_to_date = False
        mock_discover.return_value = mock_vcs_client

        commit(['/usr/local/bin/commit', 'This is the message'])

        self.assertEqual(call(1), mock_exit.call_args)

    @patch('committer.actions.detect_vcs_client')
    def test_should_use_first_argument_as_commit_message_when_committing(self, mock_discover):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.everything_was_up_to_date = True
        mock_discover.return_value = mock_vcs_client

        commit(['/usr/local/bin/commit', 'This is the message'])

        self.assertEqual(call('This is the message'), mock_vcs_client.commit.call_args)
