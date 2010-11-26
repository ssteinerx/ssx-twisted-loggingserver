from zope.interface import implements

from twisted.python import usage
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin

from loggingserver.loggingservicerunner import makeService
import logging.config

class Options(usage.Options):
    synopsis = "[options]"
    longdesc = "Create a sink for SocketHandler log records and a web server to display them."
    optParameters = [
        ['cachesize', 'c', 30],
        ['interface', 'i', '127.0.0.1'],
        ['receiveport', 'r', logging.config.DEFAULT_LOGGING_CONFIG_PORT],
        ['webport', 'w', logging.config.DEFAULT_LOGGING_CONFIG_PORT+1],
    ]

class LoggingServiceMaker(object):
    implements(IServiceMaker, IPlugin)

    tapname = "loggingserver"
    description = "Logging server."
    options = Options

    def makeService(self, config):
        return makeService(config)

serviceMaker = LoggingServiceMaker()