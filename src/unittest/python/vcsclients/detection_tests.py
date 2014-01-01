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

from mock import Mock, call, patch

import unittest
import unittest_support

from committer.vcsclients import detection
from committer.errors import NotExecutableError, NoRepositoryDetectedError, TooManyRepositoriesError


class ListAvailableVcsClientsTests(unittest_support.TestCase):

    def test_should_return_three_vcs_clients(self):

        actual_vcs_clients = detection._list_available_vcs_clients()
        actual_count_of_repositories = len(actual_vcs_clients)

        self.assertEqual(3, actual_count_of_repositories)

    def test_should_find_git_vcs_client(self):
        actual_vcs_clients = detection._list_available_vcs_clients()

        self.assertEqual('Git', actual_vcs_clients[0].name)

    def test_should_find_mercurial_vcs_client(self):
        actual_vcs_clients = detection._list_available_vcs_clients()

        self.assertEqual('Mercurial', actual_vcs_clients[1].name)

    def test_should_find_subversion_vcs_client(self):
        actual_vcs_clients = detection._list_available_vcs_clients()

        self.assertEqual('Subversion', actual_vcs_clients[2].name)


class EnsureExecutableTests(unittest.TestCase):
    def test_should_raise_exception_if_vcs_client_not_executable(self):
        mock_vcs_client = Mock()
        mock_vcs_client.is_executable.return_value = False

        self.assertRaises(NotExecutableError, detection._ensure_executable, mock_vcs_client)

    def test_should_return_vcs_client_object_when_executable(self):
        mock_vcs_client = Mock()
        mock_vcs_client.is_executable.return_value = True

        self.assertEqual(mock_vcs_client, detection._ensure_executable(mock_vcs_client))


class DiscoverVcsClientForCurrentDirectoryTests(unittest_support.TestCase):
    @patch('committer.vcsclients.detection._detect_all_vcs_clients')
    def test_should_raise_exception_when_no_repository_detected(self, mock_detect_all_vcs_clients):
        mock_detect_all_vcs_clients.return_value = None

        self.assertRaises(NoRepositoryDetectedError, detection.detect_vcs_client)

    @patch('committer.vcsclients.detection._detect_all_vcs_clients')
    def test_should_raise_exception_when_more_than_one_repository_detected(self, mock_detect_all_vcs_clients):
        mock_detect_all_vcs_clients.return_value = [self.create_mock_vcs_client(), self.create_mock_vcs_client()]

        self.assertRaises(TooManyRepositoriesError, detection.detect_vcs_client)

    @patch('committer.vcsclients.detection._detect_all_vcs_clients')
    def test_should_return_detected_vcs_client(self, mock_detect_all_vcs_clients):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_detect_all_vcs_clients.return_value = [mock_vcs_client]

        actual_vcs_client = detection.detect_vcs_client()

        self.assertEqual(actual_vcs_client, mock_vcs_client)


class DetectTests(unittest_support.TestCase):
    @patch('committer.vcsclients.detection._list_available_vcs_clients')
    def test_should_return_vcs_client_module_when_detect_returns_true(self, mock_find):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.detect.return_value = True
        mock_find.return_value = [mock_vcs_client]

        actual_detected_vcs_clients = detection._detect_all_vcs_clients()

        self.assertEqual([mock_vcs_client], actual_detected_vcs_clients)
        self.assertEqual(call(), mock_vcs_client.detect.call_args)

    @patch('committer.vcsclients.detection._list_available_vcs_clients')
    def test_should_return_no_vcs_client_module_when_detection_fails(self, mock_find):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.detect.return_value = False
        mock_find.return_value = [mock_vcs_client]

        actual_detected_vcs_clients = detection._detect_all_vcs_clients()

        self.assertEqual([], actual_detected_vcs_clients)
        self.assertEqual(call(), mock_vcs_client.detect.call_args)
