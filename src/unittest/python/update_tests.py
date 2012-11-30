from mock import call, patch

import unittest_support


from committer.errors import WrongUsageError
from committer.actions import perform_update


class UpdateTests (unittest_support.TestCase):
    def test_should_show_usage_when_more_than_one_argument (self):
        self.assertRaises(WrongUsageError, perform_update, ['/usr/local/bin/update', '-m'])

    @patch('committer.actions.discover_working_repository')
    def test_should_discover_current_working_repository (self, mock_discover):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_discover.return_value = mock_vcs_client

        perform_update(['/usr/local/bin/update'])

        self.assertEquals(call(), mock_discover.call_args)

    @patch('committer.actions.discover_working_repository')
    def test_should_use_vcs_client_to_update_repository (self, mock_discover):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_discover.return_value = mock_vcs_client

        perform_update(['/usr/local/bin/update'])

        self.assertEquals(call(), mock_vcs_client.update.call_args)
