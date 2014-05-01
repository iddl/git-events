import time, sys
from config import Config
from notificationGetter import NotificationGetter
from notificationDisplayer import NotificationDisplayerFactory
from notificationFilter import *


class GitEvents:
    def __init__(self):
        self.notifications = NotificationGetter(settings)
        self.notification_system = NotificationDisplayerFactory().get()
        event_types = [CommentEvent(), PullRequestEvent()]
        self.notification_filter = NotificationFilter(event_types)

    def get_updates(self):
        current_feed = self.notifications.get_unread()
        events = self.notification_filter.extract(current_feed)
        for event in events:
            self.notification_system.display(event['message'])

if __name__ == "__main__":

    try:
        settings = Config().get()
    except Exception:
        print("Please configure cfg.ini before starting")
        sys.exit(1)

    updates = GitEvents()
    polling_interval = settings.getint('Connection','pollinginterval')

    while(True):
        updates.get_updates()
        time.sleep(polling_interval*60)
