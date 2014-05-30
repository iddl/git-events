from eventFilter import *
from messages import Messages

#using dependency injection on this
class Core:
    def __init__(self, messages, settings, notification_system, notifications):
        self.messages = messages
        self.settings = settings
        self.notification_system = notification_system
        self.notifications = notifications

        self.last_update_at = datetime.datetime.utcnow()
        self.time_filter = TimeFilter()
        event_types = [CommentEvent(), PullRequestEvent(), PushEvent()]
        event_filters = [self.time_filter]
        self.notification_filter = EventFilter(event_types, event_filters)

    def tick(self):
        self.time_filter.set_interval(self.last_update_at)
        self.last_update_at = datetime.datetime.utcnow()
        current_feed = self.notifications.get_unread()
        events = self.notification_filter.extract(current_feed)
        for event in events:
            self.notification_system.display(event['message'])

    def start(self):
        self.messages.print_success(Messages.RUNNING)
        polling_interval = self.settings.getint('Connection','pollinginterval')

        while(True):
            self.tick()
            time.sleep(polling_interval*60)

