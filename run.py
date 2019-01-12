import logging
from logging.handlers import RotatingFileHandler

from pyphercises.app import app

if __name__ == "__main__":

    # initialize the log handler
    logHandler = RotatingFileHandler('weatherApp.log', maxBytes=1000, backupCount=1)
    
    # set the log handler level
    logHandler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)

    app.logger.addHandler(logHandler)    

    app.run(host="0.0.0.0")