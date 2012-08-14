import unittest

from mock import call, patch

from committer import perform, commit

class Test (unittest.TestCase):
    @patch('__builtin__.exit')
    @patch('committer.vcsclients.util.call')
    @patch('committer.vcsclients.util.check_call')
    def test (self, mock_check, mock_call, mock_exit):
        mock_check.return_value = 0

        perform(commit, ['/usr/local/bin/commit', 'This is the commit message'], 'usage information')
        
        self.assertEquals([call(['git', 'pull']),
                           call(['git', 'commit', '-a', '-m', 'This is the commit message']),
                           call(['git', 'push'])],
                          mock_call.call_args_list)
        self.assertEquals(call(['git', '--version']), mock_check.call_args)
        self.assertEquals(call(0), mock_exit.call_args)


if __name__ == '__main__':
    unittest.main()