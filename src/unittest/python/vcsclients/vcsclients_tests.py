from mock import Mock, call, patch

import unittest
import unittest_support

from committer import vcsclients
from committer.errors import (NotExecutableException,
                              NoRepositoryDetectedException,
                              TooManyRepositoriesException)
 
class FindTests (unittest_support.TestCase):
    def test_should_find_mercurial_vcs_client (self):
        actual_vcs_clients = vcsclients._find()
        actual_count_of_repositories = len(actual_vcs_clients)
        
        self.assertEquals(3, actual_count_of_repositories)
    
    def test_should_find_git_vcs_client (self):
        actual_vcs_clients = vcsclients._find()
        
        self.assertTrue(vcsclients.git in actual_vcs_clients)
    
    def test_should_find_mercurial_vcs_client (self):
        actual_vcs_clients = vcsclients._find()
        
        self.assertTrue(vcsclients.mercurial in actual_vcs_clients)
    
    def test_should_find_subversion_vcs_client (self):
        actual_vcs_clients = vcsclients._find()
        
        self.assertTrue(vcsclients.subversion in actual_vcs_clients)


class EnsureExecutableTests (unittest.TestCase):
    def test_should_raise_exception_if_vcs_client_not_executable(self):
        mock_vcs_client = Mock()
        mock_vcs_client.is_executable.return_value = False
        
        self.assertRaises(NotExecutableException, vcsclients.ensure_executable, mock_vcs_client)

    def test_should_return_vcs_client_object_when_executable (self):
        mock_vcs_client = Mock()
        mock_vcs_client.is_executable.return_value = True
        
        self.assertEqual(mock_vcs_client, vcsclients.ensure_executable(mock_vcs_client))


class DiscoverWorkingRepository (unittest_support.TestCase):
    @patch('committer.vcsclients._detect_repositories')
    def test_should_raise_exception_when_no_repository_detected (self, mock_detect_repositories):
        mock_detect_repositories.return_value = None
        
        self.assertRaises(NoRepositoryDetectedException, vcsclients.discover_working_repository)

    @patch('committer.vcsclients._detect_repositories')
    def test_should_raise_exception_when_more_than_one_repository_detected (self, mock_detect_repositories):
        mock_detect_repositories.return_value = [self.create_mock_vcs_client(), self.create_mock_vcs_client()]
        
        self.assertRaises(TooManyRepositoriesException, vcsclients.discover_working_repository)

    @patch('committer.vcsclients._detect_repositories')
    def test_should_return_detected_vcs_client (self, mock_detect_repositories):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_detect_repositories.return_value = [mock_vcs_client]
        
        actual_vcs_client = vcsclients.discover_working_repository()
        
        self.assertEqual(actual_vcs_client, mock_vcs_client)


class DetectTests (unittest_support.TestCase):
    @patch('committer.vcsclients._find')
    def test_should_return_vcs_client_module_when_detect_returns_true (self, mock_find):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.detect.return_value = True
        mock_find.return_value = [mock_vcs_client]
        
        actual_detected_vcs_clients = vcsclients._detect_repositories()
        
        self.assertEquals([mock_vcs_client], actual_detected_vcs_clients)
        self.assertEquals(call(), mock_vcs_client.detect.call_args)

    @patch('committer.vcsclients._find')
    def test_should_return_no_vcs_client_module_when_detection_fails (self, mock_find):
        mock_vcs_client = self.create_mock_vcs_client()
        mock_vcs_client.detect.return_value = False
        mock_find.return_value = [mock_vcs_client]
        
        actual_detected_vcs_clients = vcsclients._detect_repositories()
        
        self.assertEquals([], actual_detected_vcs_clients)
        self.assertEquals(call(), mock_vcs_client.detect.call_args)