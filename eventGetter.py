import requests, re

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

    def get_etag(self, endpoint):
        request_headers = {'Authorization' : "token " + self.authorization}
        etagrequest = requests.get(endpoint, headers=request_headers)
        etag = etagrequest.headers["etag"]
        return etag

    def get_unread(self):
        request_headers = dict()
        request_headers['Authorization'] = "token " + self.authorization
        request_headers['If-None-Match'] = self.etag

        request = requests.get(self.endpoint, headers=request_headers)

        if request.status_code == requests.codes.ok:
            print(request.text)
            return request.json()
        elif request.status_code == 304:
            return []
        else:
            raise Exception("Error getting new notifications.")
