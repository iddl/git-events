class EventReader:

    def __init__(self, event):
        self.event = event

    def get_type(self):
        return self.event['subject']['type']

    def get_title(self):
        return self.event['subject']['title']


class CommentEvent:

    @staticmethod
    def matches(event):
        if event.get_type() == 'Comment':
            return True
        else:
            return False

    @staticmethod
    def extract(event):
        formatted_event = dict()
        formatted_event['type'] = event.get_type()
        formatted_event['message'] = 'Comment: ' + event.get_title()
        return formatted_event


class PullRequestEvent:

    @staticmethod
    def matches(event):
        if event.get_type() == 'PullRequest':
            return True
        else:
            return False

    @staticmethod
    def extract(event):
        formatted_event = dict()
        formatted_event['type'] = event.get_type()
        formatted_event['message'] = 'Pull Request: ' + event.get_title()
        return formatted_event


class NotificationFilter:

    def __init__(self, event_types):
        self.event_types = event_types

    def extract(self, feed):
        events = []

        for event in feed:
            readable_event = EventReader(event)
            for event_type in self.event_types:
                if event_type.matches(readable_event):
                    events.append(event_type.extract(readable_event))

        return events