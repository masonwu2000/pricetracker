"""
Contains a function for getting credentials for a database.
"""
from configparser import ConfigParser


def config():
    parser = ConfigParser()
    parser.read("database.ini")

    db = {}
    if parser.has_section("postgresql"):
        params = parser.items("postgresql")
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("No postgresql credentials found")

    return db
