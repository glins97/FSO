from src.process_module import Process
from src.resource_module import ResourceManager
from src.memory_module import MemoryManager

class MiniOS():

    def __init__(self) -> None:
        self.processes = {}

        self.memory_manager = MemoryManager(
            blocks={
                Process.TYPE_USER: 960,
                Process.TYPE_REALTIME: 64,
            }
        )

        self.resource_manager = ResourceManager(
            scanners=1,
            printers=2,
            modems=1,
            sata_devices=2,
        )

    def _parse_process_description(self, start_time, priority, cpu_time, memory_blocks, printer, scanner, modem, disk):
        start_time = int(start_time)
        priority = int(priority)
        cpu_time = int(cpu_time)
        memory_blocks = int(memory_blocks)
        printer = int(printer)
        scanner = int(scanner)
        modem = int(modem)
        disk = int(disk)

        return start_time, priority, cpu_time, memory_blocks, printer, scanner, modem, disk

    def show_available_memory(self):
        print('\nAvailable memory:')

        for priority, memory_blocks in self.memory_manager.available_memory_blocks.items():
            print(f'\t{Process.get_priority_description(priority)}: {memory_blocks}')
     
    def load_processes(self, path):
        # reads input file
        data = []
        with open(path) as f:
            data = f.read().split('\n')

        # parses read data
        processes = []
        for id, line in enumerate(data):
            start_time, priority, cpu_time, memory_blocks, printer, scanner, modem, disk = self._parse_process_description(*line.split(','))
            
            if not self.memory_manager.get_available_blocks(memory_blocks, priority):
                print(f'ERROR::\tfailed to spawn process p{id}. No more memory avaialble for priority {priority}')
                continue

            processes.append(
                Process(
                    pid=f'p{id}',
                    start_time=start_time,
                    priority=priority,
                    cpu_time=cpu_time,
                    memory_blocks=memory_blocks,
                    printer=printer,
                    scanner=scanner,
                    modem=modem,
                    disk=disk,
                )
            )
            
            # assign memory blocks
            self.memory_manager.assign_memory_blocks(memory_blocks, processes[-1])

        # save to OS list of processes
        for process in processes:
            self.processes[process.pid] = process

        return processes
   
    def start(self):
        self.show_available_memory()
        self.resource_manager.show_available_resources()
