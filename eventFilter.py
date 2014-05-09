class CommentEvent:

    @staticmethod
    def matches(event):
        if event["type"] == 'PullRequestReviewCommentEvent':
            return True
        else:
            return False

    @staticmethod
    def extract(event):
        formatted_event = dict()
        comment_author = event["actor"]["login"]
        comment_content = event["payload"]["comment"]["body"]
        comment_repo = event["repo"]["name"]
        formatted_event['message'] = comment_author + ' commented on ' + comment_repo + ': ' + comment_content
        return formatted_event


class PullRequestEvent:

    @staticmethod
    def matches(event):
        if event["type"] == 'PullRequestEvent':
            return True
        else:
            return False

    @staticmethod
    def extract(event):
        formatted_event = dict()
        pullrequest_author = event["actor"]["login"]
        pullrequest_title = event["payload"]["pull_request"]["title"]
        formatted_event['message'] = pullrequest_author + ' made a pull request: ' + pullrequest_title
        return formatted_event

class PushEvent:

    @staticmethod
    def matches(event):
        if event["type"] == 'PushEvent':
            return True
        else:
            return False

    @staticmethod
    def extract(event):
        formatted_event = dict()
        push_author = event["actor"]["login"]
        push_commits = event["payload"]["commits"]
        push_branch = event["payload"]["ref"]
        push_commit_messages = list(map(lambda commit: commit["message"], push_commits))
        formatted_event["message"] = push_author + ' pushed to ' + push_branch + ': '
        for message in push_commit_messages:
            formatted_event["message"] += (message + ' ')
        return formatted_event


class EventFilter:

    def __init__(self, event_types):
        self.event_types = event_types

    def extract(self, feed):
        print(feed)
        events = []

        for event in feed:
            for event_type in self.event_types:
                 if event_type.matches(event):
                      events.append(event_type.extract(event))

        return events