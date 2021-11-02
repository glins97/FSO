import random
import unittest

from src.filesystem_module import FileSystemManager
from src.process_module import Process

from lib.utils import get_random_bytes

class TestFileSystem(unittest.TestCase):

    def test_create_succeeds_with_plenty_space(self):
        fsm = FileSystemManager(base_dir='src/drives/tests/')
        process = Process(pid='test_suite', type=Process.TYPE_REALTIME) 
        
        path = 'filesystem/test_create_succeeds_with_plenty_space.txt'
        write_content = get_random_bytes(n=1024)

        # if test file already exists, delete it
        _, read = fsm.read(path)
        if read:
            fsm.delete(path, process)

        # checks if file does not exist
        _, read = fsm.read(path)
        self.assertFalse(read, 'test file initially does not exist')

        # checks if file is created
        fsm.create(write_content, path, process)
        read_content, read = fsm.read(path)
        self.assertTrue(read, 'test file is created successfully')
        
        # checks if file is created correctly
        self.assertEqual(read_content, write_content, 'written test file contains correct content')

        # deletes test file
        fsm.delete(path, process)

    def test_create_succeeds_with_exact_space(self):
        fsm = FileSystemManager(base_dir='src/drives/tests/', blocks=1)
        process = Process(pid='test_suite', type=Process.TYPE_REALTIME) 

        path = 'filesystem/test_create_succeeds_with_exact_space.txt'
        write_content = get_random_bytes(n=8192)

        # if test file already exists, delete it
        _, read = fsm.read(path)
        if read:
            fsm.delete(path, process)

        # checks if file does not exist
        _, read = fsm.read(path)
        self.assertFalse(read, 'test file initially does not exist')

        # checks if file is created
        fsm.create(write_content, path, process)
        read_content, read = fsm.read(path)
        self.assertTrue(read, 'test file is created successfully')
        
        # checks if file is created correctly
        self.assertEqual(read_content, write_content, 'written test file contains correct content')

        # deletes test file
        fsm.delete(path, process)

    def test_create_fails_no_space(self):
        fsm = FileSystemManager(base_dir='src/drives/tests/', blocks=1)
        process = Process(pid='test_suite', type=Process.TYPE_REALTIME) 

        # attempts to create a file too large
        path = 'filesystem/test_create_no_space_fails.txt'
        write_content = get_random_bytes(n=16384)
        created = fsm.create(write_content, path, process)
        
        # checks process failed
        self.assertFalse(created, 'create fails when out of space')

        # deletes test file
        fsm.delete(path, process)

    def test_create_fails_no_space_2(self):
        fsm = FileSystemManager(base_dir='src/drives/tests/', blocks=2)
        process = Process(pid='test_suite', type=Process.TYPE_REALTIME) 

        # fills block #1
        path = 'filesystem/test_create_no_space_2_fails.txt'
        write_content = get_random_bytes(n=1024)
        created = fsm.create(write_content, path, process)
        self.assertTrue(created, 'create succeds when there is space')

        # fills block #2
        path_2 = 'filesystem/test_create_no_space_2_fails_2.txt'
        write_content_2 = get_random_bytes(n=1024)
        created = fsm.create(write_content_2, path_2, process)
        self.assertTrue(created, 'create succeds when there is space 2')

        # attemps to fill block #3, but should fail
        path_3 = 'filesystem/test_create_no_space_2_fails_3.txt'
        write_content_3 = get_random_bytes(n=1024)
        created = fsm.create(write_content_3, path_3, process)
        
        # checks if process failed
        self.assertFalse(created, 'create fails when there are no more available blocks')

        # deletes test files
        fsm.delete(path, process)
        fsm.delete(path_2, process)

    def test_read(self):
        fsm = FileSystemManager(base_dir='src/drives/tests/')
        process = Process(pid='test_suite', type=Process.TYPE_REALTIME) 
        
        path = 'filesystem/test_read_succeeds.txt'
        write_content = get_random_bytes(n=1024)

        # if test file already exists, delete it
        _, read = fsm.read(path)
        if read:
            fsm.delete(path, process)

        # checks if file does not exist
        _, read = fsm.read(path)
        self.assertFalse(read, 'test file initially does not exist')

        # checks if file is created
        fsm.create(write_content, path, process)
        read_content, read = fsm.read(path)
        self.assertTrue(read, 'test file is created successfully')
        
        # checks if file is read correctly
        self.assertEqual(read_content, write_content, 'test read file contains correct content')

        # deletes test file
        fsm.delete(path, process)

    def test_update(self):
        fsm = FileSystemManager(base_dir='src/drives/tests/')
        process = Process(pid='test_suite', type=Process.TYPE_REALTIME) 

        path = 'filesystem/test_update_succeeds.txt'
        write_content = get_random_bytes(n=1024)
        write_content_2 = get_random_bytes(n=1024)

        # makes sure contents are different
        while write_content == write_content_2:
            write_content_2 = get_random_bytes(n=1024)
        self.assertNotEqual(write_content, write_content_2, 'test update contents are different')

        # if test file already exists, delete it
        _, read = fsm.read(path)
        if read:
            fsm.delete(path, process)

        # checks if file does not exist
        _, read = fsm.read(path)
        self.assertFalse(read, 'test file initially does not exist')

        # checks if file is created
        fsm.create(write_content, path, process)
        _, read = fsm.read(path)
        self.assertTrue(read, 'test file is created successfully')

        # updates file 
        fsm.update(write_content_2, path, process)
        read_content, read = fsm.read(path)
        self.assertTrue(read, 'test file is updated successfully')
        
        # checks if file is read correctly
        self.assertEqual(read_content, write_content_2, 'test read file contains correct content')

        # deletes test file
        fsm.delete(path, process)

    def test_delete_succeeds(self):
        fsm = FileSystemManager(base_dir='src/drives/tests/')
        process = Process(pid='test_suite', type=Process.TYPE_REALTIME) 
        path = 'filesystem/test_delete_succeeds.txt'
        write_content = get_random_bytes(n=1024)

        # if test file already exists, delete it
        _, read = fsm.read(path)
        if read:
            fsm.delete(path, process)

        # checks if file does not exist
        _, read = fsm.read(path)
        self.assertFalse(read, 'test file initially does not exist')

        # checks if file is created
        fsm.create(write_content, path, process)
        _, read = fsm.read(path)
        self.assertTrue(read, 'test file is created successfully')
        
        # deletes test file
        fsm.delete(path, process)
        
        # checks if test file is deleted successfully
        _, read = fsm.read(path)
        self.assertFalse(read, 'test file is deleted successfully')
        
    
    def test_delete_fails_no_permission(self):
        fsm = FileSystemManager(base_dir='src/drives/tests/')
        path = 'filesystem/test_delete_fails_no_permission.txt'

        user_process = Process('test_suite__user', type=Process.TYPE_USER)
        realtime_process = Process('test_suite__realtime', type=Process.TYPE_REALTIME)
        write_content = get_random_bytes(n=1024)

        # if test file already exists, delete it
        _, read = fsm.read(path)
        if read:
            fsm.delete(path, realtime_process)

        # checks if file does not exist
        _, read = fsm.read(path)
        self.assertFalse(read, 'test file initially does not exist')

        # checks if file is created
        fsm.create(write_content, path, realtime_process)
        _, read = fsm.read(path)
        self.assertTrue(read, 'test file is created successfully')
        
        # deletes test file
        fsm.delete(path, user_process)
        
        # checks if test file is deleted successfully
        _, read = fsm.read(path)
        self.assertTrue(read, 'test file is not deleted')
        
        # deletes test file
        fsm.delete(path, realtime_process)

    
if __name__ == '__main__':
    unittest.main()