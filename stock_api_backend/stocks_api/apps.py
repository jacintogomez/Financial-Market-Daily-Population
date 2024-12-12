from django.apps import AppConfig
import logging
import sys

class StocksApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stocks_api'

    def ready(self):
        logger=logging.getLogger('custom')
        sys.stdout=StreamToLogger(logger,logging.DEBUG)

class StreamToLogger:
    def __init__(self,logger,level):
        self.logger=logger
        self.level=level

    def write(self,msg):
        if msg.strip():
            self.logger.log(self.level,msg)

    def flush(self):
        pass