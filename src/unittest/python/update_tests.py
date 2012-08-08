from mock import call, patch

import unittest_support


from committer import errors, update


class UpdateTests (unittest_support.TestCase):
    @patch('committer.repositories.detect')
    def test_should_return_with_zero_when_updating (self, mock_detect):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]

        update.perform(['/usr/local/bin/update'], 'usage information')
        

    @patch('committer.repositories.detect')
    def test_should_update_on_update (self, mock_detect):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        update.perform(['/usr/local/bin/update'], 'usage information')
        
        self.assertEquals(call(), mock_repository.update.call_args)
