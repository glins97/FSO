import json

class Process():
    TYPE_REALTIME = 0
    TYPE_USER = 3

    def __init__(self, pid, start_time=0, priority=0, cpu_time=0, memory_blocks=16, printer=False, scanner=False, modem=False, disk=0):
        self.pid = pid
        self.start_time = start_time
        self.priority = priority
        self.cpu_time = cpu_time
        self.memory_blocks = memory_blocks
        self.printer = printer
        self.scanner = scanner
        self.modem = modem
        self.disk = disk

    @property
    def type(self):
        return Process.get_priority_description(self.priority)

    @staticmethod
    def get_priority_description(priority):
        if priority == 0:
            return 'TYPE__REALTIME'
        if priority == 3:
            return 'TYPE__USER'
        if priority == 3:
            return f'TYPE__PRIO_{priority}'

    def __str__(self):
        return json.dumps({
            attr: getattr(self, attr) for attr in ['pid', 'start_time', 'priority', 'cpu_time', 'memory_blocks', 'printer', 'scanner', 'modem', 'disk', ]
        }, indent=2)


