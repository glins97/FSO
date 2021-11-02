from src.filesystem_module import FileSystemManager
from src.memory_module import MemoryManager

class Dispatcher():

    def __init__(self) -> None:
        self.filesystem_manager = FileSystemManager(base_dir='src/drives/sda1/')
        self.memory_manager = MemoryManager()