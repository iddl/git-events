import requests
from datetime import datetime

GITHUB_NOTIFICATION_ENDPOINT = 'https://api.github.com/notifications'


class NotificationGetter:

    def __init__(self, config):
        self.authorization = config["Account"]["accesstoken"]
        self.last_poll = datetime.utcnow()

    def get_unread(self):
        events = self.get(self.last_poll)
        self.last_poll = datetime.utcnow()
        return events

    def get(self, start_time=None):
        request_params = {}
        request_headers = {'Authorization' : "token " + self.authorization}
        if start_time is not None:
            request_params['since'] = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        request = requests.get(GITHUB_NOTIFICATION_ENDPOINT, params=request_params, headers=request_headers)
        print(request.text)
        return request.json()
