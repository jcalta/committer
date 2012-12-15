import unittest_support

from committer import errors


class ErrorsTests (unittest_support.TestCase):
    def test_should_use_the_given_properties (self):
        actual_exception = errors.CommitterError('message', 123)

        self.assertEqual('message\n', actual_exception.message)
        self.assertEqual(123, actual_exception.error_code)

    def test_should_raise_exception_when_given_return_code_is_zero (self):
        self.assertRaises(Exception, errors.CommitterError, 'message', 0)

    def test_should_raise_exception_when_error_code_is_greater_than_127 (self):
        self.assertRaises(Exception, errors.CommitterError, 'message', 128)

    def test_no_repository_detected_should_use_the_given_properties (self):
        actual_exception = errors.NoRepositoryDetectedError()

        self.assertEqual('No repository detected.\n', actual_exception.message)
        self.assertEqual(100, actual_exception.error_code)

    def test_show_usage_information_should_use_the_given_properties (self):
        actual_exception = errors.WrongUsageError()

        self.assertEqual("""
Wrong usage, please use the committer commands as expected.

usage:
    ci "message"     commits all changes
    st               shows all changes
    up               updates the current directory

""", actual_exception.message)
        self.assertEqual(1, actual_exception.error_code)

    def test_too_many_repositories_detected_should_use_the_given_properties (self):
        mock_repositories = [self.create_mock_vcs_client(), self.create_mock_vcs_client()]
        actual_exception = errors.TooManyRepositoriesError(mock_repositories)

        self.assertEqual('Detected more than one repository: MockRepository, MockRepository\n', actual_exception.message)
        self.assertEqual(101, actual_exception.error_code)

    def test_no_executable_should_use_the_given_properties (self):
        mock_repository = self.create_mock_vcs_client()
        actual_exception = errors.NotExecutableError(mock_repository)

        self.assertEqual('MockRepository command line client "mock-vcs-command" not executable.\n', actual_exception.message)
        self.assertEqual(102, actual_exception.error_code)
