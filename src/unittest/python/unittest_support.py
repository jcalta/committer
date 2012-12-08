import unittest

from mock import Mock
from committer.vcsclients import AbstractVcsClient

class TestCase (unittest.TestCase):
    def create_mock_vcs_client (self):
        mock_vcs_client = Mock(AbstractVcsClient)
        mock_vcs_client.command = 'mock-vcs-command'
        mock_vcs_client.name = 'MockRepository'
        return mock_vcs_client    