import unittest

from mock import call, patch

import unittest_support

from committer import errors


class ErrorsTests (unittest_support.TestCase):
    def test_should_use_the_given_properties (self):
        actual_exception = errors.CommitterException('message', 123)
        
        self.assertEquals('message\n', actual_exception.message)
        self.assertEquals(123, actual_exception.error_code)


    def test_should_raise_exception_when_given_return_code_is_zero (self):
        self.assertRaises(Exception, errors.CommitterException, 'message', 0)


    def test_should_raise_exception_when_error_code_is_greater_than_127 (self):
        self.assertRaises(Exception, errors.CommitterException, 'message', 128)


    def test_no_repository_detected_should_use_the_given_properties (self):
        actual_exception = errors.NoRepositoryDetectedException()
        
        self.assertEquals('No repository detected.\n', actual_exception.message)
        self.assertEquals(100, actual_exception.error_code)


    def test_too_many_repositories_detected_should_use_the_given_properties (self):
        mock_repositories = [self.create_mock_repository(), self.create_mock_repository()]
        actual_exception = errors.TooManyRepositoriesException(mock_repositories)
        
        self.assertEquals('More than one repository detected: MockRepository, MockRepository\n', actual_exception.message)
        self.assertEquals(101, actual_exception.error_code)


    def test_no_executable_should_use_the_given_properties (self):
        mock_repository = self.create_mock_repository()
        actual_exception = errors.NotExecutableException(mock_repository)
        
        self.assertEquals('MockRepository command line client "repository-command" not executable.\n', actual_exception.message)
        self.assertEquals(102, actual_exception.error_code)