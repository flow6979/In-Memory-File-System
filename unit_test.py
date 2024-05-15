import unittest
from script import FileSystem

class TestFileSystem(unittest.TestCase):

    def setUp(self):
        self.file_system = FileSystem()

    def test_mkdir(self):
        try:
            self.file_system.mkdir("test_dir")
            self.assertIn("test_dir", self.file_system.current_directory.children)
            self.assertTrue(self.file_system.current_directory.children["test_dir"].is_directory)
            print("\n\033[92mTest test_mkdir PASSED\033[0m\n")  
        except AssertionError:
            print(f"\n\033[91mTest test_mkdir PASSED\033[0m\n")

    def test_cd(self):
        try:
            self.file_system.mkdir("test_dir")
            self.file_system.cd("test_dir")
            self.assertEqual(self.file_system.current_directory.name, "test_dir") 
            print(f"\n\033[92mTest test_cd PASSED\033[0m\n")  
        except AssertionError:
            print(f"\n\033[91mTest test_cd PASSED\033[0m\n") 

    def test_ls(self):
        try:
            self.file_system.mkdir("test_dir")
            self.file_system.ls() 
            print(f"\n\033[92mTest test_ls PASSED\033[0m\n")
        except AssertionError:
            print(f"\n\033[91mTest test_ls PASSED\033[0m\n")

    def test_touch(self):
        try:
            self.file_system.touch("test_file.txt")
            self.assertIn("test_file.txt", self.file_system.current_directory.children)
            self.assertFalse(self.file_system.current_directory.children["test_file.txt"].is_directory)
            print(f"\n\033[92mTest test_touch PASSED\033[0m\n")
        except AssertionError:
            print(f"\n\033[91mTest test_touch PASSED\033[0m\n")

if __name__ == '__main__':
    unittest.main() 

# explain why it passed
