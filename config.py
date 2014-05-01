import configparser

CFG_FILE = 'cfg.ini'
config = configparser.ConfigParser()


class Config:

    def __init__(self):
        self.configuration = configparser.ConfigParser()

    def create_default_config(self):
        self.configuration['Connection'] = { 'pollinginterval' : 1 }
        self.configuration['Account'] = { 'token' : ''}
        with open(CFG_FILE, 'w') as configfile:
            self.configuration.write(configfile)

    def get(self):
        self.configuration.read(CFG_FILE)
        s = self.configuration.sections()
        if len(self.configuration.sections()) == 0:
            self.create_default_config()
            raise Exception("Please configure git notifications")
        return self.configuration
