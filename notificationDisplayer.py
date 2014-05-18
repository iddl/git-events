import subprocess, os, sys
from messages import Messages

class NotificationDisplayer:

    def __init__(self):
        iconame = "assets/octocat.png"
        self.icon = os.path.abspath(iconame)

class NotificationDisplayerNotifySend(NotificationDisplayer):

    def __init__(self):
        NotificationDisplayer.__init__(self)
        return

    def display(self, message):
        subprocess.Popen(['notify-send', '-i', self.icon, message])

class NotificationDisplayerGrowlnotify(NotificationDisplayer):

    def __init__(self):
        NotificationDisplayer.__init__(self)
        return

    def display(self, message):
        # to be implemented
        pass

class NotificationDisplayerFactory:

    def __init__(self):
        return

    def get(self):
        if sys.platform == 'linux':
            return NotificationDisplayerNotifySend()
        elif sys.platform == 'darwin':
            return NotificationDisplayerGrowlnotify()
        else:
            raise Exception(Messages.INCOMPATIBLE_OS)