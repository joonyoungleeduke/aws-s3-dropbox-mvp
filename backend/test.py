import unittest
import os
from FileProcessor import FileProcessor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dummy_file_name = "dummy_file.txt"
dummy_file_path = os.path.join(BASE_DIR, dummy_file_name)
dummy_file_contents = "dummy_file_contents"
dummy_bucket_name = os.environ.get("DUMMY_BUCKET_NAME")
processor = FileProcessor(bucket=dummy_bucket_name)

with open(dummy_file_path, 'w') as f:
    f.write(dummy_file_contents)


class TestFileProcessor(unittest.TestCase):

    def setUp(self):
        processor.delete_all()

    def tearDown(self):
        processor.delete_all()

    def test_all(self):
        files = processor.retrieve_file_names()
        self.assertEqual(len(files), 0)
        processor.upload_file(dummy_file_name, dummy_file_path)
        files = processor.retrieve_file_names()
        self.assertEqual(len(files), 1)
        file_url_fetch = processor.fetch_file_url(dummy_file_name)
        self.assertTrue(file_url_fetch is not None)
        processor.delete_file(dummy_file_name)


if __name__ == "__main__":
    unittest.main()
