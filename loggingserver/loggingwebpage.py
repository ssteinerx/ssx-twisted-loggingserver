"""
This module contains the html the logging server uses to display its
status.
"""

htmlpage = """
<html>
  <head>
    <meta http-equiv="refreshNOT" content="5" />
    <title>Logging Server Status Page</title>
    <style type="text/css">
        body {
          margin-top: 10px;
          margin-bottom: 10px;
          margin-right: 10px;
          margin-left: 10px;
          font-family: verdana, arial, helvetica, sans-serif;
        }

        h2, h4 {
          text-align: center;
          padding-top: 0px;
          padding-bottom: 0px;
          margin: 2px;
        }

        table {
          margin-left: auto;
          margin-right: auto;
          padding: 0;
          border: 1px solid black;
          border-collapse: collapse;
          border-spacing: 0;
        }

        table.logs {
          table-layout: fixed;
        }

        tr {
          font-family: "Lucida Console", monospace;
          font-size: 10pt;
        }

        tr.critical {
          background-color: red;
          color: yellow;
          text-decoration: blink;
        }

        tr.error {
          background-color: #ff3300;  /* red */
          color: yellow;
        }

        tr.warn {
          background-color: #ffff99; /* yellow */
          color: black;
        }

        tr.info {
          background-color: lightgreen;
          color: black;
        }

        tr.debug {
          background-color: aquamarine;
          color: black;
        }

        tr.header {
          font-family: verdana, arial, helvetica, sans-serif;
          font-size: 10pt;
        }

        td.cell {
          border: 1px solid black;
          padding: 2px 2px;
        }
    </style>
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
"""
