import configparser
from messages import Messages

CFG_FILE = 'cfg.ini'

class Config:

    def __init__(self):
        self.configuration = configparser.ConfigParser()

    def save_config(self):
        with open(CFG_FILE, 'w') as configfile:
            self.configuration.write(configfile)

    def create_default_config(self):
        self.configuration['Connection'] = { 'pollinginterval' : 1 }
        self.configuration['Account'] = { 'token' : ''}
        self.save_config()

    # need to use a key value based approach to avoid
    # explosion of methods
    def set_token(self, token):
        self.configuration['Account']['accesstoken'] = token
        self.save_config()

    # ditto
    def set_interval(self, interval):
        self.configuration['Connection']['pollinginterval'] = str(interval)
        self.save_config()

    def get(self):
        self.configuration.read(CFG_FILE)
        if len(self.configuration.sections()) == 0:
            self.create_default_config()
            raise Exception(Messages.CONFIGURATION_ERROR)
        return self.configuration
