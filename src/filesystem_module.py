import os
import pickle

class Block():

    def __init__(self, id, size, owner=None, path=None, content=None):
        self.id = id
        self.size = size
        
        self.owner = owner
        self.path = path
        if content is None:
            self.content = [None] * size

    @property
    def is_free(self):
        return self.owner is None and self.path is None

class FileSystemManager():
    LOCK_PATH = 'filesystem_manager.lock'

    def __init__(self, base_dir='src/drives/sda1/', blocks=1024, block_size=8192, use_lock=False):
        self.BASE_DIR = base_dir
        self.BLOCK_SIZE = block_size

        self.max_available_blocks = blocks
        self.blocks = [Block(id=id, size=block_size) for id in range(blocks)]
        self.use_lock = use_lock

        if os.path.exists(self.LOCK_PATH) and self.use_lock:
            with open(self.LOCK_PATH, 'rb') as f:
                self.paths = pickle.load(f)
        else:
            self.paths = {}

    def save_paths_lock(self):
        if not self.use_lock:
            return

        with open(self.LOCK_PATH, 'wb') as f:
            pickle.dump(self.paths, f)

    def get_available_blocks(self, size):
        if size / self.BLOCK_SIZE > self.max_available_blocks:
            return []

        blocks = []
        remaining_size = size
        for block in self.blocks:
            if block.is_free:
                remaining_size -= self.BLOCK_SIZE
                blocks.append(block)
            else:
                blocks = []
                remaining_size = size

            if remaining_size <= 0:
                return blocks

        raise Exception('size available suggest there is enough space, but it was NOT found')

    def get_utilization_map(self):
        return [ (block if not block.is_free else None) for block in self.blocks ]

    def load_block(self, path, starting_block, size):
        for block in self.blocks[starting_block:starting_block + size]:
            block.path = path
            block.owner = None
        self.paths[path] = self.blocks[starting_block:starting_block + size]

    def create(self, bytes, path, owner):
        return self._write(bytes, path, owner)

    def update(self, bytes, path, owner):
        return self._write(bytes, path, owner)

    def _write(self, bytes, path, owner):
        path = self.BASE_DIR + path
        if len(bytes) / self.BLOCK_SIZE > self.max_available_blocks:
            return False

        blocks = self.get_available_blocks(len(bytes))
        try:
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

            with open(path, 'wb') as f:
                f.write(bytes)
            
            for block in blocks:
                block.path = path
                block.owner = owner
            
            self.max_available_blocks -= len(blocks)
            self.paths[path] = blocks
            self.save_paths_lock()

            return True
        except Exception as e:
            return False

    def read(self, path):
        path = self.BASE_DIR + path
        try:
            with open(path, 'rb') as f:
                return f.read(), True
        except Exception as e:
            return bytes(), False

    def delete(self, path, process):
        path = self.BASE_DIR + path
        try:
            if path in self.paths:
                blocks = self.paths[path]
                if blocks and process.type < blocks[0].owner.type:
                    return False
                
                for block in blocks:
                    block.owner = None
                    block.path = None

                del self.paths[path]
                self.save_paths_lock()

                self.max_available_blocks += len(blocks)
            os.remove(path)
            return True
        except:
            pass

    def show_disk_usage(self):
        print('Disk utilization:')
        for block in self.blocks:
            if block.is_free:
                print('\tBlock {}: [   ]'.format(block.id))
            else:
                print('\tBlock {}: [ {} ]'.format(block.id, block.path))