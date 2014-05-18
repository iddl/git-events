import subprocess, os

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

class NotificationDisplayerFactory:

    def __init__(self):
        return

    def get(self):
        return NotificationDisplayerNotifySend()