#!/usr/bin/python

from dotenv import load_dotenv

import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".flaskenv"))

MEDIA_PATH = os.getenv("MEDIA_PATH")

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    
"""
logging_config = {
    "version": 1,
    "disable_existing_loggers": "false",
    "formatters": {
        "basic": {
            "class": "logging.Formatter",
            "datefmt": "%I:%M:%S",
            "format": "%(asctime)s %(levelname)s %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "basic",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "basic",
            "filename": "log",
            "mode": "w",
            "encoding": "utf-8"
        }
    },

    "loggers": { },

    "root": {
        "handlers": ["file"],
        "level": "DEBUG"
    }
}
"""