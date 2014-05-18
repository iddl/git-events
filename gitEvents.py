import sys
import datetime
from config import Config
from eventGetter import EventGetterFactory
from notificationDisplayer import NotificationDisplayerFactory
from eventFilter import *

def abort(message):
    print(message)
    sys.exit(1)

class GitEvents:
    def __init__(self):
        try:
            self.notification_system = NotificationDisplayerFactory().get()
        except Exception:
            abort("Your OS is not compatible with Git events")

        try:
            self.notifications = EventGetterFactory().get(settings)
        except Exception:
            abort("I'm unable to access your GitHub account, please check your internet connection and GitHub access token.")

        self.last_update_at = datetime.datetime.utcnow()
        self.timeFilter = TimeFilter()
        event_types = [CommentEvent(), PullRequestEvent(), PushEvent()]
        event_filters = [self.timeFilter]
        self.notification_filter = EventFilter(event_types, event_filters)

    def get_updates(self):
        self.timeFilter.set_interval(self.last_update_at)
        self.last_update_at = datetime.datetime.utcnow()
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
        time.sleep(polling_interval*10)
