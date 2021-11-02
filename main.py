
from src.mini_os import MiniOS

os = MiniOS()
os.load_processes('processes.txt')
os.start()
