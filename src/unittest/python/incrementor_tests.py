import unittest

from mock import Mock, call, patch
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

