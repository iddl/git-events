import os, atexit, signal, sys
import argparse
from messages import messages_provider
from processes import processes_provider
from core import Core

running_process= processes_provider.get()
messages = messages_provider.get()

def stop():
    if not running_process.is_running():
        messages.abort(messages.NOT_RUNNING)
    pid = running_process.get_pid()
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception as processKillException:
        pass
    cleanup()
    messages.print_success(messages.STOPPED)

def cleanup():
    running_process.unregister_process()

# should be perfected using a double-fork
def daemonize():
    pid = os.fork()
    if pid == 0:
        atexit.register(cleanup)
        running_process.register_process()
        signal.signal(signal.SIGTERM, cleanup)
        messages.print_success(messages.RUNNING)
        messages.use_logfile()
    else:
        sys.exit(0)

def start(daemon=True):
    if running_process.is_running():
        messages.abort(messages.WAS_RUNNING)

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

