#!/usr/bin/python

from app import app
import logging.config
from config import logging_config

if __name__ == "__main__":
    logging.config.dictConfig(logging_config)
    app.run(host='0.0.0.0')
