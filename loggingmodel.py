'''
 $Id$

This module defines the logging server system 'model'
code, sort of like the model of an MVC pattern of thinking
about the logging server system.
'''

##
# November 7, 2010 -- ssteinerX
#
# Made queueSize configurable instead of a constant so different servers
# could have different sized windows.
#
# Changed default size to 30 since refreshing 200 in the demo was just annoying.
##

AUTHOR = "Doug Farrell"
REVISION = "$Rev$"

# system modules
import datetime

class LoggingServerModel(object):
    '''This class defines what data will be saved and available to
    the logging system viewers and controllers.
    '''

    def __init__(self, queueSize=30):
        '''Constructor for the class, initializes the class level
        variables.
        '''
        self._startTime = datetime.datetime.now()
        self._logRecordsTotal = 0L
        self._logrecords = []
        self._queueSize = queueSize

    def __iter__(self):
        '''Provide a reverse iterator so logrecords are provided
        in newest to oldest order.
        '''
        index = len(self._logrecords)
        while index > 0:
            index -= 1
            yield self._logrecords[index]

    def _getStartTime(self):
        '''Get the time the logging server was started'''
        return self._startTime.strftime("%Y-%m-%d %H:%M:%S")
    starttime = property(_getStartTime)

    def _getUpTime(self):
        '''Get the current uptime of the logging server minus the
        microseconds'''
        diff = (datetime.datetime.now() - self._startTime).__str__()
        return diff[:diff.find('.')]
    uptime = property(_getUpTime)

    def _getLogRecordsTotal(self):
        return self._logRecordsTotal
    logRecordsTotal = property(_getLogRecordsTotal)

    def _getQueueSize(self):
        return self._queueSize
    queueSize = property(_getQueueSize)

    def logRecordHandler(self, logrecord):
        '''This method adds the logrecord to the sliding
        window of logrecords coming into the logging server.
        '''
        logrecords = self._logrecords
        logrecords.append(logrecord)
        if len(logrecords) > self._queueSize:
            logrecords.pop(0)
        self._logRecordsTotal += 1


model = LoggingServerModel()