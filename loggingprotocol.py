'''
 $Id$
 
This module defines the logging protocol the server receives network messages
from the logging client. Where logging.handlers.SocketHandler
is the client side of a network based Python logging solution, this
provides the server side interface for what the SocketHandler module 
produces.
'''

AUTHOR = "Doug Farrell"
REVISION = "$Rev$"

# python system modules
import logging
import logging.config
import cPickle                 # use cPickle for speed
import struct
from ConfigParser import ConfigParser

# third party system modules
import twisted
from twisted.application import service, internet
from twisted.internet import protocol
from twisted.web import resource, server as webserver

# local modules
from loggingwebpage import htmlpage
from loggingmodel import model


class LoggingProtocol(twisted.internet.protocol.Protocol):
    '''This class encapsulates the actual handling of the data 
    received by the protocol. It builds up the message till it can
    peel off a log message, and then calls the defined
    logger.handle() so the Python logging system can then handle
    the message.
    '''
    LONG_INT_LENGTH = 4
    
    def __init__(self):
        '''Constructor for our derived Protocol class. This configures
        the logging system for the server and sets up some instance
        variables.
        '''
        # configure the logging system
        logging.config.fileConfig('loggingserver.conf',
                                  {"processlog" : "process.log"})
        self._logger = logging.getLogger("logging server")
        self._buffer = ""
        
    def dataReceived(self, data):
        '''This method accumulates the data received till
        we have a complete log message. Then it pulls the log message 
        out and to logger.handle as a logrecord. This
        method is called by the Protocol parent class when data is
        received from the socket attached to this protocol. This 
        method has to handle possible multiple messages per buffer 
        and partial messages per buffer.

        Parameters:
        data           string of data received by the socket this
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
                        self._logger.handle(logRecord)
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
        self._buffer = ""
            
    def handle_quit(self):
        self.transport.loseConnection()


class LoggingFactory(twisted.internet.protocol.Factory):
    '''This factory creates the loggingProtocol when built'''
    protocol = LoggingProtocol
    

class LoggingService(twisted.application.internet.TCPServer):
    '''This class encapsulates our TCP service, tying it to a 
    port number and to the protocol that will handle the received
    messages, in this case an instance of LoggingProtocol
    '''
    def __init__(self):
        twisted.application.internet.TCPServer.__init__(self,
            logging.handlers.DEFAULT_TCP_LOGGING_PORT,
            LoggingFactory())
        self.setName("Logging Server")
        
        
class LoggingServerWebResource(twisted.web.resource.Resource):
    '''This class defines the entry point for the logging server
    status home page. This page provides a view of what's going
    on inside the logging server.
    '''
    def render_GET(self, request):
        formatter = logging.Formatter(
            fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")
        data = {}
        data["starttime"] = model.starttime
        data["uptime"] = model.uptime
        data["logrecordstotal"] = model.logRecordsTotal
        # create list of all log records
        html = '''<tr class="%s"><td>%s</td></tr>'''
        rows = []
        for logrecord in model:
            if logrecord.levelno == logging.CRITICAL:
                rows.append(html % ("critical",
                    formatter.format(
                        logrecord).replace(' ', '&nbsp;')))
            if logrecord.levelno == logging.ERROR:
                rows.append(html % ("error",
                    formatter.format(
                        logrecord).replace(' ', '&nbsp;')))
            if logrecord.levelno == logging.WARN:
                rows.append(html % ("warn",
                    formatter.format(
                        logrecord).replace(' ', '&nbsp;')))
            if logrecord.levelno == logging.INFO:
                rows.append(html % ("info",
                    formatter.format(
                        logrecord).replace(' ', '&nbsp;')))
            if logrecord.levelno == logging.DEBUG:
                rows.append(html % ("debug",
                    formatter.format(
                        logrecord).replace(' ', '&nbsp;')))
        data["all"] = ''.join(rows)
        return htmlpage % data
    
class LoggingServerWebService(twisted.application.internet.TCPServer):
    '''This class encapsulates the createion of the TCP service that
    provides the HTTP webserver for the logging servers status page.
    '''
    def __init__(self):
        webRoot = twisted.web.resource.Resource()
        webRoot.putChild('', LoggingServerWebResource())
        site = twisted.web.server.Site(webRoot)
        internet.TCPServer.__init__(self,
                logging.handlers.DEFAULT_TCP_LOGGING_PORT + 1, site)
        self.setName("Logging Server Web Server")