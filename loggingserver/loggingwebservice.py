import logging.handlers

from twisted.application import internet

import twisted.internet

from loggingmodel import model
from loggingwebpage import htmlpage


class LoggingServerWebResource(twisted.web.resource.Resource):
    """This class defines the entry point for the logging server
    status home page. This page provides a view of what's going
    on inside the logging server.
    """
    # November 7, 2010 -- ss -- only initialize once for the class
    formatter = logging.Formatter(
        fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    html = """<tr class="%s"><td>%s</td></tr>"""

    def render_GET(self, request):
        data = {
            "starttime"         : model.starttime,
            "uptime"            : model.uptime,
            "logrecordstotal"   : model.logRecordsTotal,
        }

        # create list of all log records
        rows = []
        for logrecord in model:
            # November 7, 2010 -- ssteinerX, removed a bunch of silly code
            levelName = logging.getLevelName(logrecord.levelno).lower()
            text = LoggingServerWebResource.formatter.format(logrecord).replace(' ', '&nbsp;')
            rows.append(LoggingServerWebResource.html % (levelName, text))

        data["all"] = ''.join(rows)
        return htmlpage % data


class LoggingServerWebService(twisted.application.internet.TCPServer):
    """This class encapsulates the createion of the TCP service that
    provides the HTTP webserver for the logging servers status page.
    """
    def __init__(self, interface='127.0.0.1'):
        webRoot = twisted.web.resource.Resource()
        webRoot.putChild('', LoggingServerWebResource())
        site = twisted.web.server.Site(webRoot)
        # webRoot.putChild('loggingserver.css', File('loggingserver.css'))
        internet.TCPServer.__init__(self,
                logging.handlers.DEFAULT_TCP_LOGGING_PORT + 1, site, interface=interface)
        self.setName("Logging Server Web Server")
