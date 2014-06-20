from eventFilter import *
from config import config_provider
from notificationDisplayer import notifications_provider
from eventGetter import eventgetter_provider
from messages import messages_provider

messages = messages_provider.get()
notification_system = notifications_provider.get()
event_getter = eventgetter_provider.get()
settings = config_provider.get()

#using dependency injection on this
class Core:
    def __init__(self):
        self.last_update_at = datetime.datetime.utcnow()
        self.time_filter = TimeFilter()
        event_types = [CommentEvent(), PullRequestEvent(), PushEvent()]
        event_filters = [self.time_filter]
        self.notification_filter = EventFilter(event_types, event_filters)

    def tick(self):
        self.time_filter.set_interval(self.last_update_at)
        self.last_update_at = datetime.datetime.utcnow()
        current_feed = event_getter.get_unread()
        events = self.notification_filter.extract(current_feed)
        for event in events:
            notification_system.display(event['message'])

    def start(self):
        messages.print_success(messages.RUNNING)
        polling_interval = settings.getint('Connection','pollinginterval')

        while(True):
            self.tick()
            time.sleep(polling_interval*60)

