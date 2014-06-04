import os, atexit, signal, sys
import argparse
from config import Config
from bootstrap import Bootstrap
from messages import Messages
from processes import Processes
from core import Core
from eventGetter import EventGetterFactory
from notificationDisplayer import NotificationDisplayerFactory

def stop():
    runningProcess = Processes()

    if not runningProcess.is_running():
        messages.abort(Messages.NOT_RUNNING)
    pid = runningProcess.get_pid()
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception as processKillException:
        pass
    cleanup()
    messages.print_success(Messages.STOPPED)

def cleanup():
    running_process = Processes()
    running_process.unregister_process()

# should be perfected using a double-fork
def daemonize():
    running_process = Processes()

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
    settings = Config().get()
    messages = Messages()
    running_process = Processes()

    if running_process.is_running():
        messages.abort(Messages.WAS_RUNNING)

    try:
        notification_system = NotificationDisplayerFactory().get()
    except Exception as notificationSystemException:
        messages.abort(notificationSystemException)

    try:
        notifications = EventGetterFactory().get(settings)
    except Exception as eventGetterException:
        messages.abort(eventGetterException)

    core = Core(messages, settings, notification_system, notifications)

    if daemon:
        daemonize()

    core.start()


if __name__ == "__main__":

    configuration = Config()
    messages = Messages()

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('operation', metavar="[start|stop|restart]", action="store", help='Start git-events')
    parser.add_argument('--no-daemon', action="store_false", dest="daemonize", help='Do not run git-event as a daemon')
    args = parser.parse_args()

    settings = configuration.get()
    if not configuration.is_set_up():
        bootstrapper = Bootstrap(configuration)
        try:
            bootstrapper.setup()
        except Exception as boostrap_exception:
            messages.abort(Messages.SETUP_FAIL)

    if args.operation == 'start':
        start(args.daemonize)
    elif args.operation == 'restart':
        stop()
        start()
    elif args.operation == 'stop':
        stop()
    else:
        print("Invalid args")

