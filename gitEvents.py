import os, atexit, signal, sys
import argparse
from messages import *
from processes import running_process
from core import Core

def stop():
    if not running_process.is_running():
        messages.abort(Messages.NOT_RUNNING)
    pid = running_process.get_pid()
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception as processKillException:
        pass
    cleanup()
    messages.print_success(Messages.STOPPED)

def cleanup():
    running_process.unregister_process()

# should be perfected using a double-fork
def daemonize():
    pid = os.fork()
    if pid == 0:
        atexit.register(cleanup)
        running_process.register_process()
        signal.signal(signal.SIGTERM, cleanup)
        messages.print_success(Messages.RUNNING)
        messages.use_logfile()
    else:
        sys.exit(0)

def start(daemon=True):
    if running_process.is_running():
        messages.abort(Messages.WAS_RUNNING)

    core = Core()

    if daemon:
        daemonize()

    core.start()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('operation', metavar="[start|stop|restart]", action="store", help='Start git-events')
    parser.add_argument('--no-daemon', action="store_false", dest="daemonize", help='Do not run git-event as a daemon')
    args = parser.parse_args()

    if args.operation == 'start':
        start(args.daemonize)
    elif args.operation == 'restart':
        stop()
        start()
    elif args.operation == 'stop':
        stop()
    else:
        print("Invalid args")

