import sys, argparse
from config import Config
from eventGetter import EventGetterFactory
from notificationDisplayer import NotificationDisplayerFactory
from eventFilter import *
from messages import Messages

#need some refactoring in here

def abort(message=""):
    print(message)
    sys.exit(1)



class GitEvents:
    def __init__(self):
        try:
            self.notification_system = NotificationDisplayerFactory().get()
        except Exception as notificationSystemException:
            abort(notificationSystemException)

        try:
            self.notifications = EventGetterFactory().get(settings)
        except Exception as eventGetterExpection:
            abort(eventGetterExpection)

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

    configuration = Config()

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-interval', type=int, metavar="INTERVAL", nargs=1, help='set polling interval in minutes (default: 1)', dest="set_interval")
    args = parser.parse_args()

    try:
        settings = configuration.get()
    except Exception as configurationException:
        abort(configurationException)

    if args.set_interval:
        interval = args.set_interval[0]
        configuration.set_interval(interval)
        print(Messages.INTERVAL_SET)
    else:
        updates = GitEvents()
        polling_interval = settings.getint('Connection','pollinginterval')

        while(True):
            updates.get_updates()
            time.sleep(polling_interval*10)
