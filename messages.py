class Messages():

    #Status
    RUNNING = 'Git-events is now running...'

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

