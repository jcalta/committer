import unittest

from mock import Mock, call, patch
if sys.version_info[0] == 3:
    from io import StringIO
else:
    from StringIO import StringIO
from committer.incrementor import (increment_version,
                                   increment_version_string,
                                   version_is_contained_in_line)

class VersionIsContainedInLineTests (unittest.TestCase):
    def test_should_not_find_version_in_string(self):
        self.assertFalse(version_is_contained_in_line("foobar"))

    def test_should_not_find_version_in_string_starting_with_version(self):
        self.assertFalse(version_is_contained_in_line("version_tralala='Hello'"))
        
    def test_should_find_version_in_string_starting_with_version(self):
        self.assertTrue(version_is_contained_in_line("version='0.1.2'"))
        
    def test_should_find_version_in_string_starting_with_version(self):
        self.assertTrue(version_is_contained_in_line("version = '0.1.2'"))

    def test_should_find_version_in_string_starting_with_version_and_some_blanks(self):
        self.assertTrue(version_is_contained_in_line('version   =  "1.2.3"'))

class IncrementVersionStringTests (unittest.TestCase):
    def test_increment_version_with_one_number(self):
        version = "version = '1'"

        actual_incremented_version = increment_version_string(version)

        self.assertEqual("version = '2'", actual_incremented_version)

    def test_increment_version_with_two_numbers(self):
        version = "version = '0.1'"

        actual_incremented_version = increment_version_string(version)

        self.assertEqual("version = '0.2'", actual_incremented_version)

    def test_increment_version_with_three_numbers(self):
        version = "version = '0.1.2'"

        actual_incremented_version = increment_version_string(version)

        self.assertEqual("version = '0.1.3'", actual_incremented_version)

    def test_increment_version_with_three_numbers_and_double_quotes(self):
        version = 'version = "0.1.2"'

        actual_incremented_version = increment_version_string(version)

        self.assertEqual('version = "0.1.3"', actual_incremented_version)

class IncrementVersionTests (unittest.TestCase):
    @patch('committer.incrementor.os.rename')
    @patch('__builtin__.open')
    def test_should_increment_version_in_build_py (self, mock_open, mock_rename):
        original_content = StringIO()
        mock_destination_file = Mock()
        mock_open.side_effects = [original_content, mock_destination_file] 
        
        increment_version()

        # TODO: assert correct file contents        
        self.assertEqual([call('build.py', 'r'), call('build.py.new', 'w')], mock_open.call_args_list)
        self.assertEqual([call('build.py.new', 'build.py')], mock_rename.call_args_list)
