
class MemoryBlock():

    def __init__(self, id, size, owner=None):
        self.id = id
        self.size = size
        self.owner = owner

    @property
    def is_free(self):
        return self.owner is None

class MemoryManager():

    def __init__(self, blocks={}, block_size=1048576) -> None:
        self.blocks = {
            priority: MemoryManager._create_memory_blocks(blocks[priority], block_size) for priority in blocks
        }
        self.available_memory_blocks = {
            priority: blocks[priority] for priority in blocks
        }

    @staticmethod
    def _create_memory_blocks(n, block_size):
        return [MemoryBlock(i, block_size) for i in range(n)]

        
    def get_available_blocks(self, n, priority):
        if priority > 0:
            priority = 3

        if n > self.available_memory_blocks[priority]:
            return []

        blocks = []
        remaining_blocks = n
        for block in self.blocks[priority]:
            if block.is_free:
                remaining_blocks -= 1
                blocks.append(block)
            else:
                blocks = []
                remaining_blocks = n

            if remaining_blocks <= 0:
                return blocks

        raise Exception('size available suggest there is enough space, but it was NOT found')


    def assign_memory_blocks(self, n, process):
        priority = process.priority
        if priority > 0:
            priority = 3

        try:
            blocks = self.get_available_blocks(n, priority)
            for block in blocks:
                block.owner = process
            
            self.available_memory_blocks[priority] -= len(blocks)
            return True
        except Exception as e:
            print('ERROR::\tfailed to write content to memory block')
            return False