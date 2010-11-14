'''
Main logging program that implements the socket based logging server.

Can be invoked with:
    twistd  --pidfile=loggingserver.pid \
            --logfile=loggingserver.log \
            --python=loggingserver.py

Also see loggingservicerunner.py which contains

'''

##
# Removed "Wing IDE" __main__ function, didn't work for me anyway.  Making
# a twistd plugin instead.
##

import os
from twisted.application import service

import loggingprotocol
import loggingwebservice

from loggingservicerunner import makeService

makeService()
