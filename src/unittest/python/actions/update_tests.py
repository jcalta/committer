from mock import call, patch

import unittest_support

from committer.errors import WrongUsageError
from committer.actions import update


class UpdateTests (unittest_support.TestCase):
    def test_should_show_usage_when_more_than_one_argument(self):
        self.assertRaises(WrongUsageError, update, ['/usr/local/bin/update', '-m'])

    @patch('committer.actions.detect_vcs_client')
    def test_should_detect_vcs_client(self, mock_discover):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_discover.return_value = mock_vcs_client

        update(['/usr/local/bin/update'])

        self.assertEqual(call(), mock_discover.call_args)

    @patch('committer.actions.detect_vcs_client')
    def test_should_use_vcs_client_to_update_repository(self, mock_discover):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_discover.return_value = mock_vcs_client

        update(['/usr/local/bin/update'])

        self.assertEqual(call(), mock_vcs_client.update.call_args)
