'''
 $Id$
 
This module defines the logging server system 'model'
code, sort of like the model of an MVC pattern of thinking 
about the logging server system.
'''

AUTHOR = "Doug Farrell"
REVISION = "$Rev$"

# system modules
import datetime

class LoggingServerModel(object):
    '''This class defines what data will be saved and available to
    the logging system viewers and controllers.
    '''
    MAX_SIZE = 200

    def __init__(self):
        '''Constructor for the class, initializes the class level
        variables.
        '''
        self._startTime = datetime.datetime.now()
        self._logRecordsTotal = 0L
        self._logrecords = []
        
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
    
    def logRecordHandler(self, logrecord):
        '''This method adds the logrecord to the sliding
        window of logrecords coming into the logging server.
        '''
        logrecords = self._logrecords
        logrecords.append(logrecord)
        if len(logrecords) > LoggingServerModel.MAX_SIZE:
            logrecords.pop(0)
        self._logRecordsTotal += 1


model = LoggingServerModel()