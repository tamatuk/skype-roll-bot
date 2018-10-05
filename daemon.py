import os
import signal
import sys
import traceback
import time

from subprocess import Popen

from main import create_server

COMMANDS = ['start', 'stop', 'restart']


def setsavedpid(pid):
    f = open("pid.txt", "w")
    f.write(str(pid))
    
def getsavedpid():
    try:
        f = open("pid.txt", "r")
        return int(f.read())
    except IOError:
        return 0
    
def deletesavepid():
    try:
        os.remove("pid.txt")
    except OSError:
        pass
    
def getstartedpid():        
    """ Check For the existence of a unix pid. """
    pid = getsavedpid()
    try:
        os.kill(pid, 0)
    except OSError:
        return 0
    else:
        return pid

def kill_process(pid):
    os.kill(pid, signal.SIGKILL)

def start():
    if not getstartedpid():
        P = Popen([
            'python', os.path.abspath(__file__),
            'daemon',
        ])
        pid = P.pid
        setsavedpid(pid)
        print('Server started (pid {}).'.format(pid))
    else:
        print('Server already started.')

def stop():
    pid = getsavedpid()
    if pid:
        try:
            kill_process(pid)
            print('Server stoped (pid {})'.format(pid))
        except:
            print('Server not started (pid {})'.format(pid))
        deletesavepid()
    else:
        print('Server not started')

def restart():
    stop()
    time.sleep(1)
    start()
    time.sleep(1)

def daemon():
    try:
        create_server()
    except:
        traceback.print_exc()

if __name__ == "__main__":
    num = len(sys.argv)
    if sys.argv[1] in (COMMANDS + ['daemon']):
        cmd = sys.argv[1]
        globals()[cmd]()
    else:
        print('Error: invalid command')
        print('Usage: python daemon.py {%s}.' % '|'.join(COMMANDS))
