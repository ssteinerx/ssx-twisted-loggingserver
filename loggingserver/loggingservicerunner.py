'''
Main logging program that implements the socket based logging server.
'''

##
# Removed "Wing IDE" __main__ function, didn't work for me anyway.  Making
# a twistd plugin instead.
##

import os
from twisted.application import service

import loggingprotocol
import loggingwebservice

def makeService(config):
    # create an application instance
    application = service.Application("LoggingServer")

    # create the logging service
    loggingService = loggingprotocol.LoggingService()
    loggingService.setServiceParent(application)

    # create the logging server web status page server
    loggingServiceWebServer = loggingwebservice.LoggingServerWebService()
    loggingServiceWebServer.setServiceParent(application)

