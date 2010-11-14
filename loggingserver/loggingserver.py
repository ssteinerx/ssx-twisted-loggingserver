'''
Main logging program that implements the socket based logging server.
'''

import os
from twisted.application import service

import loggingprotocol
import loggingwebservice

# create an application instance
application = service.Application("LoggingServer")

# create the logging service
loggingService = loggingprotocol.LoggingService()
loggingService.setServiceParent(application)

# create the logging server web status page server
loggingServiceWebServer = loggingwebservice.LoggingServerWebService()
loggingServiceWebServer.setServiceParent(application)

# this section allows the server to run within the wingide debugger
if __name__ == "__main__":
    from twisted.scripts.twistd import run
    try:
        os.unlink('twistd.pid')
    except OSError:
        pass
    run()