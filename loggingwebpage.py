'''
 $Id$
 
This module contains the html the logging server uses to display it's
status.
'''

AUTHOR = "Doug Farrell"
REVISION = "$Rev$"

# the html code that makes up the logging servers status page
htmlpage = '''
<html>
  <head>
    <meta http-equiv="refresh" content="5" />
    <title>Logging Server Status Page</title>
    <link rel="stylesheet" type="text/css"
          href="http://localhost/loggingserver.css" />
  </head>
  <body>
    <h4>Logging Server Status Page</h4>
    <table width="50%%">
      <tr class="header">
        <td class="cell">Logging Server Start Time</td>
        <td class="cell">%(starttime)s</td>
      </tr>
      <tr class="header">
        <td class="cell">Logging Server Uptime</td>
        <td class="cell">%(uptime)s</td>
      </tr>
      <tr class="header">
        <td class="cell">Log Records Total</td>
        <td class="cell">%(logrecordstotal)s</td>
      </tr>
    </table width="95%%">
    <!-- table of most recent log records -->
    <h4>Most Recent Log Records</h4>
    <table>
      %(all)s
    </table>
  </body>
</html>
'''