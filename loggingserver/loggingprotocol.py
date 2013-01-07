"""
This module provides a Twisted Service that handles the output of
Python's built-in logging.handlers.SocketHandler.

logging.handlers.SocketHandler is the source, this is the sink.
"""
##
# November 13, 2010
#
# Rewrote LoggingProtocol class to simplify dataReceived significantly and
# remove some repeated len() calls and other redundant calculations.
#
# Generally simplified and, I'm sure, sped up the data handling.
##

##
# November 7, 2010 -- ssteinerX
#
# Issue 1 at the google tracker requests to have the server available on a
# different port.  I added a parameter to the LoggingServerWebService to
# allow specification of a different interface
##

##
# November 7, 2010 -- ssteinerx
#
# Removed a whole ton of code from the LoggingServerWebResource.render_GET
# HTML generator by using logging's getLevelName() function instead of
# switching out on the error level
##

import logging.config
from cPickle import loads
from struct import unpack

import twisted
from twisted.internet.protocol import Protocol
from twisted.application.internet import TCPServer
from twisted.python import log  # so we can log to Twisted's separate log

import yaml

observer = log.PythonLoggingObserver()
observer.start()

# local modules
from loggingmodel import model

##
# configure the logging system *once*
##
loggerConfig = yaml.load(
"""
version: 1
formatters:
  general:
    datefmt: '%Y-%m-%d %H:%M:%S'
    format: '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
handlers:
  hlogfile:
    class: logging.FileHandler
    level: NOTSET
    formatter: general
    filename: 'process.log'
loggers:
  logfile:
    level: NOTSET
    handlers: [hlogfile]
    qualname: (logfile)
    propagate: 0
    parent: root
root:
  level: NOTSET
  handlers: [hlogfile]
  qualname: (root)
  propagate: 1
"""
)

# pprint(loggerConfig)
logging.config.dictConfig(loggerConfig)

# Constant, length of the header length (an old-style 4 byte long integer)
LONG_INT_LEN = 4


class LoggingProtocol(Protocol):
    """Encapsulates the actual handling of the data received by the
    protocol. It collects all incoming data, building and forwarding complete
    log records as they arrive.
    """

    def __init__(self):
        """Get a "loggingserver" logger, and set up our buffer and record
        instance variables.
        """
        log.msg("Creating new LoggingProtocol object")
        self.logger = logging.getLogger("loggingserver")
        self.buffer = ""
        self.buffer_len = self.full_buffer_len = 0
        self.rec_len = None

    def dataReceived(self, data):
        """Called whenever there's data available in the socket.

        Pulls the newly received data from the socket, adds it to what we've
        already got, then checks to see whether we've got enough to start
        processing a new record.

        If so, we build as much of the log record as we can and, whenever we
        have a complete one, pass it off to Python's logging system.
        """

        ##
        # First, paste the recieved data onto what we have and compute the
        # buffer's length only once rather than every time we need it.
        ##
        self.buffer += data
        self.buffer_len = len(self.buffer)

        ##
        # Keep processing the buffer, peeling off logging records, till we
        # no longer have a complete record, then exit.  We'll get called again
        # as soon as there's more data available.
        ##
        while True:
            ##
            # If we've not yet gotten the record length for the next record,
            # and we have enough data to get it, do so.
            ##
            if not self.rec_len and self.buffer_len >= LONG_INT_LEN:
                self.rec_len = unpack(">L", self.buffer[:LONG_INT_LEN])[0]
                self.full_buffer_len = LONG_INT_LEN + self.rec_len

            ##
            # If we've gotten the length, and there's enough data in the
            # buffer to build our record, do so.
            #
            # Otherwise, we're done (for now).
            ##
            if (self.rec_len and
                self.buffer_len >= self.full_buffer_len):
                ##
                # get the pickled log message, from the end of the length bytes
                # to the end of full_buffer_len i.e. just the data
                ##
                logPickle = self.buffer[LONG_INT_LEN : self.full_buffer_len]

                ##
                # Create an actual log record from the data
                ##
                logRecord = logging.makeLogRecord(loads(logPickle))

                ##
                # Send the completed log record where it needs to go
                ##
                log.msg("LoggingProtocol: logging new record")
                self.logger.handle(logRecord)
                model.logRecordHandler(logRecord)

                ##
                # Adjust our buffer to point past the end of what we just
                # processed and recompute the length
                ##
                self.buffer = self.buffer[self.full_buffer_len:]
                self.buffer_len = len(self.buffer)

                ##
                # Unset self.rec_len and self.full_buffer_len since we don't
                # yet know the length of the next one.  When we loop around,
                # we'll take care of that if we've got enough data to work on.
                ##
                self.rec_len = self.full_buffer_len = None
            else:
                ##
                # otherwise, we either don't know the length,
                # or don't have a complete record, done for now
                ##
                break

    def connectionLost(self, reason):
        log.msg("connectionLost called")
        self.buffer = ""

    def handle_quit(self):
        log.msg("handle_quit called")
        self.transport.loseConnection()


class LoggingFactory(twisted.internet.protocol.Factory):
    """Factory that creates the LoggingProtocol object"""
    protocol = LoggingProtocol


class LoggingService(TCPServer):
    """Encapsulates our TCP service, tying it to a port number and to the
    protocol that will handle the received messages, in this case an instance
    of LoggingProtocol
    """
    def __init__(self):
        twisted.application.internet.TCPServer.__init__(self,
            logging.handlers.DEFAULT_TCP_LOGGING_PORT,
            LoggingFactory())
        self.setName("Logging Server")
