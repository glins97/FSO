from src.process_module import Process
import time
import json

class QueueManager():

    def __init__(self, aging=1, max_process_age=2):
        self.aging = aging
        self.max_process_age = max_process_age
        self.queues = {
            0: [],
            1: [],
            2: [],
            3: [],
        }
        self.cpu_time = 0

    
    def add_process(self, process):
        self.queues[process.priority].append(process)

    def get_active_process(self):
        priorities = sorted(self.queues)
        for priority in priorities:
            if self.queues[priority]:
                return self.queues[priority][0]
        
        return None

    def age_processes(self):
        active_process = self.get_active_process()
        
        priorities = sorted(self.queues, reverse=True)
        for priority in priorities:
            for process in self.queues[priority]:
                if process == active_process:
                    continue

                if process.start_time > self.cpu_time:
                    process.age += self.aging 
        
                if process.age > self.max_process_age and priority > 0:
                    process.age = 0
                    self.queues[priority].remove(process)
                    self.queues[priority-1].append(process)

    def run_processes(self):
        active_process = self.get_active_process()
        if not active_process:
            return 

        active_process.cpu_time -= 1

        self.age_processes()
        
        if active_process.cpu_time <= 0:
            self.queues[active_process.priority].remove(active_process)

        self.cpu_time += 1

    def show_queues(self):
        print('\nQueues status:')
        for priority in self.queues:
            print(f'\t{Process.get_priority_description(priority, True)}: {self.queues[priority]}')