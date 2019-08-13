

"""此文件是为了兼容之前的命令
"""

import sys
from manager import cmd

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) >= 2:
        if argv[1] == 'start':
            sys.argv = ['manager.py', 'taskloop', 'start']

        if argv[1] == 'stop':
            sys.argv = ['manager.py', 'taskloop', 'stop']
    cmd()

