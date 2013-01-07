"""
Defines the logging server system 'model' code, sort of like the model of an
MVC pattern of thinking about the logging server system.
"""

##
# November 7, 2010 -- ssteinerX
#
# Made queuesize configurable instead of a constant so different servers
# could have different sized windows.
#
# Changed default size to 30 since refreshing 200 in the web page for the demo
# was just annoying.
##

import datetime


class LoggingServerModel(object):
    """Defines what data will be saved and available to the logging system
    viewers and controllers.
    """

    def __init__(self, queuesize=30):
        self._startTime = datetime.datetime.now()
        self._logRecordsTotal = 0L
        self._logrecords = []
        self._queuesize = queuesize

    def __iter__(self):
        """Provide a reverse iterator so logrecords are provided in newest to
        oldest order.
        """
        index = len(self._logrecords)
        while index > 0:
            index -= 1
            yield self._logrecords[index]

    def _getStartTime(self):
        """Get the time the logging server was started"""
        return self._startTime.strftime("%Y-%m-%d %H:%M:%S")
    starttime = property(_getStartTime)

    def _getUpTime(self):
        """Get the current uptime of the logging server sans microseconds"""
        diff = (datetime.datetime.now() - self._startTime).__str__()
        return diff[:diff.find('.')]
    uptime = property(_getUpTime)

    def _getLogRecordsTotal(self):
        return self._logRecordsTotal
    logRecordsTotal = property(_getLogRecordsTotal)

    def _getqueuesize(self):
        """Get the current size of the logging record queue"""
        return self._queuesize
    queuesize = property(_getqueuesize)

    def logRecordHandler(self, logrecord):
        """Add the logrecord to the sliding window of logrecords coming into
        the logging server.
        """
        logrecords = self._logrecords
        logrecords.append(logrecord)
        if len(logrecords) > self._queuesize:
            logrecords.pop(0)
        self._logRecordsTotal += 1


model = LoggingServerModel()
