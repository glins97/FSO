
class Process():
    TYPE_USER = 0
    TYPE_REALTIME = 3

    def __init__(self, pid, type):
        self.PID = pid
        self.type = type
