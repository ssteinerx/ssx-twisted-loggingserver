
import os
from twisted.application import service

from loggingprotocol import LoggingService
from loggingwebservice import LoggingServerWebService

def makeService(config):
    """
    Make a service that can be served as a Twisted plugin's "application"
    """

    ##
    # Create a MultiService to hold our services
    ##
    multi = service.MultiService()

    ##
    # create the logging service
    ##
    loggingService = LoggingService()
    multi.addService(loggingService)

    ##
    # Create the logging server web status page server
    ##
    loggingServiceWebServer = LoggingServerWebService()
    multi.addService(loggingServiceWebServer)

    return multi
