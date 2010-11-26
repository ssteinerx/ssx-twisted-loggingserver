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
    # create a MultiService instead of an app

    multi = service.MultiService()

    # create the logging service
    loggingService = loggingprotocol.LoggingService()
    multi.addService(loggingService)

    # create the logging server web status page server
    loggingServiceWebServer = loggingwebservice.LoggingServerWebService()
    multi.addService(loggingServiceWebServer)

    return multi
