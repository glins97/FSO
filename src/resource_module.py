from src.process_module import Process

class Resource():
    
    def __init__(self, name, process=None):
        self.name = name
        self.process = process

    def allocate(self, process):
        if process.type == Process.TYPE_REALTIME:
            print('ERROR::\trealtime processes cannot allocate resources')
            return 

        self.process = process

    def free(self):
        self.process = None

    @property
    def code(self):
        if self.process is None:
            return ''

        return self.process.__dict__[self.name]

    @property
    def available(self):
        return self.process is None


class ResourceManager():

    def __init__(self, scanners, printers, modems, sata_devices):
        self.scanners = [Resource('scanner') for _ in range(scanners)]
        self.printers = [Resource('printer') for _ in range(printers)]
        self.modems = [Resource('modem') for _ in range(modems)]
        self.sata_devices = [Resource('sata_device') for _ in range(sata_devices)]

    def has_resource_available(self, type):
        return len([r for r in self.__dict__[type] if r.available]) > 0

    def get_available_resource(self, type):
        if not self.has_resource_available(type):
            return None

        return [r for r in self.__dict__[type] if r.available][0]
    
    def show_available_resources(self):
        print('\nAvailable resources:')

        for index, r in enumerate(self.scanners):
            print(f'\tSCANNER {index}: \t' + ('AVAILABLE' if r.available else 'ALLOCATED'))

        for index, r in enumerate(self.printers):
            print(f'\tPRINTER {index}: \t' + ('AVAILABLE' if r.available else 'ALLOCATED'))

        for index, r in enumerate(self.modems):
            print(f'\tMODEM {index}: \t' + ('AVAILABLE' if r.available else 'ALLOCATED'))

        for index, r in enumerate(self.sata_devices):
            print(f'\tSATA DEVICE {index}: \t' + ('AVAILABLE' if r.available else 'ALLOCATED'))

