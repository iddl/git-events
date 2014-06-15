import configparser
from bootstrap import *
from messages import *

CFG_FILE = 'cfg.ini'

class Config:

    def __init__(self):
        self.configuration = configparser.ConfigParser()

    def save_config(self):
        with open(CFG_FILE, 'w') as configfile:
            self.configuration.write(configfile)

    def create_default_config(self):
        self.configuration['Connection'] = { 'pollinginterval' : 1 }
        self.configuration['Account'] = {}
        self.save_config()

    # should not have the section argument to resemble a
    # more generic interface
    def set_value(self, section, key, value):
        self.configuration[section][key] = value
        self.save_config()

    def get(self):
        self.configuration.read(CFG_FILE)
        if len(self.configuration.sections()) == 0:
            self.create_default_config()
        return self.configuration

    def is_set_up(self):
        if self.configuration.has_option('Account', 'username'):
            return True
        return False

configuration = Config()
settings = configuration.get()
if not configuration.is_set_up():
    bootstrapper = Bootstrap(configuration)
    try:
        bootstrapper.setup()
    except Exception as boostrap_exception:
        messages.abort(Messages.SETUP_FAIL)