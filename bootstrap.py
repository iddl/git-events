import json, requests, getpass
from messages import messages_provider

messages = messages_provider.get()

#Need to implement this using OAuth.

class Bootstrap:

    APP_NAME = "Git-events"
    AUTHORIZATIONS_ENDPOINT = "https://api.github.com/authorizations"

    def __init__(self, config):
        self.config = config

    def setup(self):
        user = input(messages.INPUT_USERNAME)
        password = getpass.getpass(messages.INPUT_PASSWORD)
        if self.using_existing_token(user, password):
            print(messages.SETUP_SUCCESS)
            return True
        if self.create_token(user, password):
            print(messages.SETUP_SUCCESS)
            return True
        return False

    def create_token(self, user, password):
        token_request = dict()
        token_request['note'] = Bootstrap.APP_NAME
        token_request['scopes'] = ["notifications" , "repo"]
        request = requests.post(Bootstrap.AUTHORIZATIONS_ENDPOINT, auth=(user, password), data=json.dumps(token_request))
        if request.status_code != requests.codes.ok:
            raise(messages.GITHUB_LOGIN_ERROR)
        data = request.json()
        self.config.set_value('Account', 'username', user)
        self.config.set_value('Account', 'accesstoken', data.token)
        return True

    def using_existing_token(self, user, password):
        request = requests.get(Bootstrap.AUTHORIZATIONS_ENDPOINT, auth=(user, password))
        if request.status_code != requests.codes.ok:
            print(messages.GITHUB_LOGIN_ERROR)
            return False
        data = request.json()
        existing_tokens = list(filter(lambda token: token["note"] == Bootstrap.APP_NAME, data))
        if not len(existing_tokens):
            return False
        self.config.set_value('Account', 'username', user)
        self.config.set_value('Account', 'accesstoken', existing_tokens[0]["token"])
        return True