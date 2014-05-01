import subprocess


class NotificationDisplayerNotifySend:

    def __init__(self):
        return

    def display(self, message):
        subprocess.Popen(['notify-send', message])


class NotificationDisplayerFactory:

    def __init__(self):
        return

    def get(self):
        return NotificationDisplayerNotifySend()