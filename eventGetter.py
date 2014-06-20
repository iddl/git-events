import requests, re, datetime, json, datetime, time
from messages import messages_provider
from config import config_provider

settings = config_provider.get()
messages = messages_provider.get()

GITHUB_EVENT_ENDPOINT = 'https://api.github.com/users/:username/received_events'

class EventGetterFactory:

    def __init__(self):
        return

    def get(self, settings):
        return EventGetterGithub(settings)

class EventGetterGithub:

    def __init__(self, config):
        self.authorization = config["Account"]["accesstoken"]
        self.username = config["Account"]["username"]
        self.endpoint = re.sub(":username", self.username, GITHUB_EVENT_ENDPOINT)
        self.etag = self.get_etag(self.endpoint)
        self.last_poll = datetime.datetime.utcnow()
        self.poll_wait = 0

    def get_etag(self, endpoint):
        request_headers = {'Authorization' : "token " + self.authorization}
        etagrequest = requests.get(endpoint, headers=request_headers)
        if etagrequest.status_code != requests.codes.ok:
            raise Exception(messages.GITHUB_API_ERROR)
        etag = etagrequest.headers["etag"]
        return etag

    def last_time_polled(self):
        return self.last_poll

    def get_unread(self):
        request_headers = dict()
        request_headers['Authorization'] = "token " + self.authorization
        request_headers['If-None-Match'] = self.etag

        time_between_polls = (datetime.datetime.utcnow() - self.last_poll).total_seconds()
        time_to_wait = self.poll_wait - time_between_polls
        if time_to_wait > 0:
            time.sleep(time_to_wait)

        request = requests.get(self.endpoint, headers=request_headers)
        self.last_poll = datetime.datetime.utcnow()

        if request.status_code == requests.codes.ok:
            self.poll_wait = int(request.headers["X-Poll-Interval"])
            return request.json()
        elif request.status_code == 304:
            self.poll_wait = int(request.headers["X-Poll-Interval"])
            return []
        else:
            raise Exception()

class EventGetterProvider:

    def __init__(self):
        self.instance = None

    def get(self):
        if self.instance is None:
            try:
                self.instance = EventGetterFactory().get(settings)
            except Exception as eventGetterException:
                messages.abort(eventGetterException)
        return self.instance

eventgetter_provider = EventGetterProvider()