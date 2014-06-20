import os

class Processes():

    PIDFILE = "git-events.pid"

    def register_process(self):
        pidfile = open(self.PIDFILE, 'w')
        pidfile.write(str(os.getpid()))
        pidfile.close()

    def unregister_process(self):
        try:
            os.remove(self.PIDFILE)
        except Exception as fileException:
            pass

    def is_running(self):
        return os.path.isfile(self.PIDFILE)

    def get_pid(self):
        if not self.is_running():
            return None
        else:
            handle = open(self.PIDFILE, 'r')
            pid = int(handle.read())
            handle.close()
            return pid


class ProcessesProvider():

    def __init__(self):
        self.instance = None

    def get(self):
        if self.instance is None:
            self.instance = Processes()
        return self.instance

processes_provider = ProcessesProvider()