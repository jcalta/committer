from mock import call, patch

import unittest_support

from committer.commit import perform
from committer.errors import WrongUsageException


class PerformTests (unittest_support.TestCase):
    def test_should_show_usage_when_more_than_one_argument (self):
        self.assertRaises(WrongUsageException, perform, ['/usr/local/bin/commit'])

    @patch('committer.commit.discover_working_repository')
    def test_should_discover_working_repository (self, mock_discover):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_discover.return_value = mock_vcs_client

        perform(['/usr/local/bin/commit', 'This is the message'])

        self.assertEquals(call(), mock_discover.call_args)

    @patch('committer.commit.discover_working_repository')
    def test_should_update_before_committing (self, mock_discover):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.commit.side_effect = Exception('commit exception')
        mock_discover.return_value = mock_vcs_client

        self.assertRaises(Exception, perform, ['/usr/local/bin/commit', 'This is the message'])

        self.assertEquals(call(), mock_vcs_client.update.call_args)

    @patch('committer.commit.discover_working_repository')
    def test_should_use_first_argument_as_commit_message (self, mock_discover):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_discover.return_value = mock_vcs_client

        perform(['/usr/local/bin/commit', 'This is the message'])

        self.assertEquals(call('This is the message'), mock_vcs_client.commit.call_args)
