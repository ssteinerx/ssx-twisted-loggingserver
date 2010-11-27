import logging.config

from zope.interface import implements

from twisted.python import usage
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin

from loggingserver.loggingservicerunner import makeService

class Options(usage.Options):
    """Options for the loggingserver"""
    synopsis = "[options]"
    longdesc = "Create a sink for SocketHandler log records and a web server "\
                "to display them."
    optParameters = [
        ['cachesize',
            'c', 30,
            "Size of the cache of log messages available via the web server."],
        ['listenport',
            'l', logging.handlers.DEFAULT_TCP_LOGGING_PORT,
            "Port on which to listen for incoming log messages."],
        ['listeninterface',
            'i', '127.0.0.1'
            "Interface on which to listen for incoming log messages."],
        ['webserverport',
            'w', logging.handlers.DEFAULT_TCP_LOGGING_PORT+1,
            "Port on which to serve the logging status page."],
        ['webserverinterface',
            's', '127.0.0.1',
            "Interface on which to serve the web page."],
    ]


class LoggingServiceMaker(object):
    implements(IServiceMaker, IPlugin)

    tapname = "loggingserver"
    description = "Socket logging server."
    options = Options

    def makeService(self, options):
        # print "options = ", options
        return makeService(options)


serviceMaker = LoggingServiceMaker()