import sys
from termcolor import colored

class Messages():

    LOGFILE = "git-events.log"

    #Status and operations
    RUNNING = 'Successfully started gitevents'
    WAS_RUNNING = 'Gitevents is already running'
    NOT_RUNNING = 'Git-events is not running'
    STOPPED = 'Successfully stopped gitevents'

    #Errors
    INCOMPATIBLE_OS = 'Your OS is not compatible with Git events'
    GITHUB_API_ERROR = 'I\'m unable to access your GitHub account, please check your internet connection and GitHub access token'
    GITHUB_LOGIN_ERROR = 'Unable to login. Wrong username/password ?'
    CONFIGURATION_ERROR = 'Please configure cfg.ini before starting'

    #Success
    ACCESS_TOKEN_SET = 'Successfully set access token'
    INTERVAL_SET = 'Successfully set polling interval'

    #Setup
    INPUT_USERNAME = 'Please type your Github account name: '
    INPUT_PASSWORD = 'Please type your Github account password: '
    SETUP_FAIL = 'Failed to create Github access token'
    SETUP_SUCCESS = 'Successfully saved access token. You are all set.'

    def abort(self, message=""):
        print(colored(message, 'red'))
        sys.exit(1)

    def print_success(self, message=""):
        print(colored(message, 'green'))

    def log(self, message=""):
        print(message)

    def use_logfile(self):
        sys.stdout = open(self.LOGFILE, 'w')
        sys.stderr = open(self.LOGFILE, 'w')


