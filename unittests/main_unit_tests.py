import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import pickle
from main import load_config, save_deed_info, upload_file_to_s3

class TestMain(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"date": "2024-07-27", "bucket_name": "test-bucket", "url": "http://example.com"}')
    def test_load_config(self, mock_file):
        config = load_config()
        self.assertEqual(config['date'],'2024-07-27')
        self.assertEqual(config['bucket_name'],'test-bucket')
        self.assertEqual(config['url'],'http://example.com')

unittest.main(argv=[''], verbosity=2, exit=False)
