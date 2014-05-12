import time, datetime

class CommentEvent:

    def matches(self, event):
        if event["type"] == 'PullRequestReviewCommentEvent':
            return True
        else:
            return False

    def extract(self, event):
        formatted_event = dict()
        comment_author = event["actor"]["login"]
        comment_content = event["payload"]["comment"]["body"]
        comment_repo = event["repo"]["name"]
        formatted_event['message'] = comment_author + ' commented on ' + comment_repo + ': ' + comment_content
        return formatted_event


class PullRequestEvent:

    def matches(self, event):
        if event["type"] == 'PullRequestEvent':
            return True
        else:
            return False

    def extract(self, event):
        formatted_event = dict()
        pullrequest_author = event["actor"]["login"]
        pullrequest_title = event["payload"]["pull_request"]["title"]
        formatted_event['message'] = pullrequest_author + ' made a pull request: ' + pullrequest_title
        return formatted_event

class PushEvent:

    def matches(self, event):
        if event["type"] == 'PushEvent':
            return True
        else:
            return False

    def extract(self, event):
        formatted_event = dict()
        push_author = event["actor"]["login"]
        push_commits = event["payload"]["commits"]
        push_branch = event["payload"]["ref"]
        push_commit_messages = list(map(lambda commit: commit["message"], push_commits))
        formatted_event["message"] = push_author + ' pushed to ' + push_branch + ': '
        for message in push_commit_messages:
            formatted_event["message"] += (message + ' ')
        return formatted_event

class TimeFilter:

    def __init__(self, start_time=datetime.datetime(1, 1, 1), end_time=datetime.datetime(9999, 12, 31)):
        self.start_time = start_time
        self.end_time = end_time

    def set_interval(self, start, end):
        self.start_time = start
        self.end_time = end

    def matches(self, event):
        event_creation_time = time.strptime(event["created_at"],"%Y-%m-%dT%H:%M:%SZ")[:6]
        event_creation_time = datetime.datetime.utcfromtimestamp(time.mktime(event_creation_time + (0,0,0)))
        if self.start_time < event_creation_time and self.end_time > event_creation_time:
            return True
        else:
            return False

class EventFilter:

    def __init__(self, event_types=[], event_filters=[]):
        self.event_types = event_types
        self.event_filters = event_filters

    def matches_filters(self, event):
        for event_filter in self.event_filters:
            if not event_filter.matches(event):
                return False
        return True

    def extract(self, feed):
        events = []

        for event in feed:
            if not self.matches_filters(event):
                continue
            for event_type in self.event_types:
                if event_type.matches(event):
                    eve = event_type.extract(event)
                    events.append(eve)

        return events