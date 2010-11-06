'''
 $Id$
 
This is just a simple test harness for the logging server.
It randomly generates log messages to send to the server till
the user hits CTRL-C. It also expects a command line parameter of 
some string, which is the "module" reporting the log message.
'''

AUTHOR = "Doug Farrell"
REVISION = "$Rev$"

import logging
import logging.config
import sys
import random
import time


if __name__ == "__main__":
    name = sys.argv[1]
    logging.config.fileConfig('loggingtest.conf',
                              {"logging_server" : "localhost"})
    log = logging.getLogger(name)
    
    try:
        y = 10 / 0
    except Exception, e:
        log.exception("divide by zero")
        
    log.critical("Here's a critical message from %s" % name)
    log.debug("hello there")
    log.info("Here's some info from logger %s" % name)
    log.critical("Here's a critical message from %s" % name)
    done = False
    while not done:
        try:
            x = random.random()
            log.info("here's the value of x = %3.2f from process %s" %
                    (x, name))
            time.sleep(x)
        except KeyboardInterrupt:
            done = True
        
    log.warn("%s is leaving the party" % name)
    print "%s is done" % name