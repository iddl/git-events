import os, sys, atexit, signal
import argparse
from config import Config
from bootstrap import Bootstrap
from messages import Messages
from processes import Processes
from core import *
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

def start():
    settings = Config().get()
    messages = Messages()
    runningProcess = Processes()

    if runningProcess.is_running():
        messages.abort(Messages.WAS_RUNNING)

    try:
        notification_system = NotificationDisplayerFactory().get()
    except Exception as notificationSystemException:
        messages.abort(notificationSystemException)

    try:
        notifications = EventGetterFactory().get(settings)
    except Exception as eventGetterException:
        messages.abort(eventGetterException)

    messages.print_success(Messages.RUNNING)

    # git-events you are cleared for takeoff, fork
    pid = os.fork()
    if(pid == 0):
        atexit.register(cleanup)
        messages.use_logfile()
        runningProcess.register_process()
        signal.signal(signal.SIGTERM, cleanup)
        core = Core(messages, settings, notification_system, notifications)
        core.start()

if __name__ == "__main__":

    configuration = Config()
    messages = Messages()

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('operation', metavar="[start|stop|restart]", action="store", help='Start git-events')
    args = parser.parse_args()

    settings = configuration.get()
    if not configuration.is_set_up():
        bootstrapper = Bootstrap(configuration)
        try:
            bootstrapper.setup()
        except Exception as boostrap_exception:
            messages.abort(Messages.SETUP_FAIL)

    if args.operation == 'start':
        start()
    elif args.operation == 'restart':
        stop()
        start()
    elif args.operation == 'stop':
        stop()
    else:
        print("Invalid args")

