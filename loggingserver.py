'''
 $Id$
 
This is the main logging program that implements the socket based
logging server.
'''

AUTHOR = "Doug Farrell"
REVISION = "$Rev$"

# system modules
import os
from twisted.application import service

# custom modules for this server
import loggingprotocol

# create an application instance
application = service.Application("LoggingServer")
    
# create the logging service
loggingService = loggingprotocol.LoggingService()
loggingService.setServiceParent(application)

# create the logging server web status page
loggingServiceWebServer = loggingprotocol.LoggingServerWebService()
loggingServiceWebServer.setServiceParent(application)
    
# this section allows the server to run within the wingide debugger
if __name__ == "__main__":
    from twisted.scripts.twistd import run
    import os
    try:
        os.unlink('twistd.pid')
    except OSError:
        pass
    run()