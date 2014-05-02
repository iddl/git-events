import requests
from email.utils import formatdate
from datetime import datetime
from time import mktime

GITHUB_NOTIFICATION_ENDPOINT = 'https://api.github.com/notifications'


class NotificationGetter:

    @staticmethod
    def toHttpDate(date):
        stamp = mktime(date.timetuple())
        return formatdate(
            timeval     = stamp,
            localtime   = False,
            usegmt      = True
        )

    def __init__(self, config):
        self.authorization = config["Account"]["accesstoken"]
        self.last_poll = datetime.utcnow()

    def get_unread(self):
        start_time = self.last_poll
        self.last_poll = datetime.utcnow()
        events = self.get(start_time)
        return events

    def get(self, start_time=None):
        request_headers = {'Authorization' : "token " + self.authorization}
        if start_time is not None:
            request_headers['If-Modified-Since'] = NotificationGetter.toHttpDate(start_time)

        request = requests.get(GITHUB_NOTIFICATION_ENDPOINT, headers=request_headers)

        if request.status_code == requests.codes.ok:
            return request.json()
        elif request.status_code == 304:
            return []
        else:
            raise Exception("Error getting new notifications.")
