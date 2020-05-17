from configparser import ConfigParser

class Config:
    """
    holds static values needed for various
    operations across the application
    """
    __CONFIG_PATH = "config"
    __CONFIG_FILENAME = "db.config"
    __parser = ConfigParser()
    __parser.read(f"{__CONFIG_PATH}/{__CONFIG_FILENAME}")
    DBHOST = __parser["database"]["host"]
    DBNAME = __parser["database"]["dbname"]
    DBUSER = __parser["database"]["user"]
    DBPASS = __parser["database"]["password"]
