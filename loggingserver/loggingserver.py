"""
Main logging program that implements the socket based logging server.

Can be invoked with:
    twistd  --pidfile=loggingserver.pid \
            --logfile=loggingserver.log \
            --python=loggingserver.py

Also see loggingservicerunner.py which contains

"""

from loggingserver.loggingservicerunner import makeService

makeService()
