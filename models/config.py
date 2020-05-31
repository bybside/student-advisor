from configparser import ConfigParser

class Config:
    """
    holds static values needed for various
    operations across the application
    """
    __CONFIG_PATH = "config"
    __CONFIG_FILENAME = "app.config"
    __parser = ConfigParser()
    __parser.read(f"{__CONFIG_PATH}/{__CONFIG_FILENAME}")
    # db config
    DBHOST = __parser["database"]["host"]
    DBNAME = __parser["database"]["dbname"]
    DBUSER = __parser["database"]["user"]
    DBPASS = __parser["database"]["password"]
    # flask config
    ENV = __parser["flask"]["env"]
    DEBUG = __parser["flask"].getboolean("debug")
    TESTING = __parser["flask"].getboolean("testing")
    # flask uses a secret key to create sessions for application users
    SECRET_KEY = __parser["flask"]["secret_key"]
