'''
This module provides a Twisted Service that handles the output of
Python's built-in logging.handlers.SocketHandler.

logging.handlers.SocketHandler is the source, this is the sink.
'''

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

# python system modules
import logging.config
import cPickle                 # use cPickle for speed
import struct

import twisted
from twisted.python import log  # so we can log to Twisted's separate log

observer = log.PythonLoggingObserver()
observer.start()

# local modules
from loggingmodel import model

# configure the logging system *once*
logging.config.fileConfig('loggingserver.conf',
                          {"processlog" : "process.log"})


class LoggingProtocol(twisted.internet.protocol.Protocol):
    '''Encapsulates the actual handling of the data received by the
    protocol. It builds up the message till it can peel off a log message, and
    then calls the defined logger.handle() so the Python logging system can
    then handle the message.
    '''
    LONG_INT_LENGTH = 4

    def __init__(self):
        '''Constructor for our derived Protocol class. This configures the
        logging system for the server and sets up some instance variables.
        '''
        self._logger = logging.getLogger("loggingserver")
        self._buffer = ""

    def dataReceived(self, data):
        '''This method accumulates the data received till we have a complete
        log message. Then it pulls the log message out and to logger.handle as
        a logrecord. This method is called by the Protocol parent class when
        data is received from the socket attached to this protocol. This
        method has to handle possible multiple messages per buffer and partial
        messages per buffer.

        Parameters:    data string of data received by the socket this
                       server is attached to contains the data sent
                       by logging.handlers.SocketHandler
        '''
        logRecord = None

        # get an alias to the LONG_INT_LENGTH
        long_int_length = LoggingProtocol.LONG_INT_LENGTH

        # paste the recieved data onto what we have
        self._buffer += data

        # keep processing the buffer till we need more data
        done = False
        while not done:
            # do we have enough data to pull off the leading big
            # endian long integer?
            if len(self._buffer) >= long_int_length:
                length = struct.unpack(">L", \
                                       self._buffer[:long_int_length])[0]

                # do we have the complete logging message?
                if len(self._buffer) >= long_int_length + length:
                    # get the pickled log message
                    logPickle = self._buffer[long_int_length : long_int_length + length]
                    logRecord = logging.makeLogRecord(cPickle.loads(logPickle))

                    # do we have a logrecord?, then handle it
                    if logRecord:
                        log.msg("passing to: self._logger == %s", self._logger)
                        self._logger.handle(logRecord)
                        log.msg("passing to: logRecordHandler")
                        model.logRecordHandler(logRecord)

                    # update the class buffer with what we have left
                    self._buffer = self._buffer[long_int_length + length:]

                # otherwise, we don't have a complete message
                else:
                    done = True
            # otherwise, don't have enough data for length value
            else:
                done = True

    def connectionLost(self, reason):
        log.msg("connectionLost called")
        self._buffer = ""

    def handle_quit(self):
        log.msg("handle_quit called")
        self.transport.loseConnection()


class LoggingFactory(twisted.internet.protocol.Factory):
    '''This factory creates the LoggingProtocol object'''
    protocol = LoggingProtocol


class LoggingService(twisted.application.internet.TCPServer):

    '''Encapsulates our TCP service, tying it to a port number and to the
    protocol that will handle the received messages, in this case an instance
    of LoggingProtocol
    '''

    def __init__(self):
        twisted.application.internet.TCPServer.__init__(self,
            logging.handlers.DEFAULT_TCP_LOGGING_PORT,
            LoggingFactory())
        self.setName("Logging Server")
