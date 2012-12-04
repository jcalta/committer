import unittest

from mock import call, patch

from committer.vcsclients import git


class PropertiesTests (unittest.TestCase):
    def test_should_have_command_property (self):
        self.assertEqual('git', git.COMMAND)

    def test_should_have_name_property (self):
        self.assertEqual('Git', git.NAME)


class CommitTests (unittest.TestCase):
    @patch('committer.vcsclients.git._git')
    def test_should_prepend_git_to_given_arguments (self, mock_git):
        
        git.commit('This is a commit message.')
        
        self.assertEqual([call('commit', '-a', '-m', 'This is a commit message.'),
                          call('push')],
                          mock_git.call_args_list)
        
        
class UpdateTests (unittest.TestCase):
    @patch('committer.vcsclients.git._git')
    def test_should_call_pull (self, mock_git):
        git.update()
        
        self.assertEqual(call('pull'), mock_git.call_args)
        

class StatusTests (unittest.TestCase):
    @patch('committer.vcsclients.git._git')
    def test_should_call_status (self, mock_git):
        git.status()
        
        self.assertEqual(call('status', '-sb'), mock_git.call_args)
        

class DetectTests (unittest.TestCase):
    @patch('os.path.isdir')
    def test_return_false_if_dot_git_directory_does_not_exist (self, mock_exists):
        mock_exists.return_value = False
        
        actual_return_value = git.detect()
        
        self.assertEqual(False, actual_return_value)
        self.assertEqual(call('.git'), mock_exists.call_args)

    @patch('os.path.isdir')
    def test_return_true_if_dot_git_directory_exists (self, mock_exists):
        mock_exists.return_value = True
        
        actual_return_value = git.detect()
        
        self.assertEqual(True, actual_return_value)
        self.assertEqual(call('.git'), mock_exists.call_args)


class IsExecutableTests (unittest.TestCase):
    @patch('committer.vcsclients.git.check_if_is_executable')
    def test_should_return_value_of_check (self, mock_check):
        mock_check.return_value = 'value from check'
        
        actual_return_value = git.is_executable()
        
        self.assertEqual('value from check', actual_return_value)

    @patch('committer.vcsclients.git.check_if_is_executable')
    def test_should_check_using_git_version (self, mock_check):
        mock_check.return_value = 'value from check'
        
        git.is_executable()
        
        self.assertEqual(call('git', '--version'), mock_check.call_args)


class GitTests (unittest.TestCase):
    @patch('committer.vcsclients.git.execute_command')
    def test_should_execute_git_using_arguments (self, mock_execute):
        git._git('arg1', 'arg2', 'arg3')
        
        self.assertEqual(call('git', 'arg1', 'arg2', 'arg3'), mock_execute.call_args)
