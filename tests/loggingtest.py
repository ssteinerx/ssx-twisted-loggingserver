'''
This is just a simple test harness for the logging server.
It randomly generates log messages to send to the server till
the user hits CTRL-C. It also expects a command line parameter of
some string, which is the "module" reporting the log message.
'''

import logging
import logging.config
import sys
import random
import time


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python loggingtest.py testername"
        print "       where 'testername' will be used in logging messages"
        print "       to identify which process produced the log entry"
        sys.exit(1)
    else:
        name = sys.argv[1]

    logging.config.fileConfig('loggingtest.conf',
                              {"logging_server" : "localhost"})
    log = logging.getLogger(name)

    log_msg_count = 0
    done = False
    while not done:
        try:
            x = random.random()
            log.info("here's the value of x = %3.2f from process %s" %
                    (x, name))
            time.sleep(x)
        except KeyboardInterrupt:
            done = True
        else:
            if (log_msg_count % 10) == 0:
                try:
                    y = 10 / 0
                except Exception, e:
                    log.exception("divide by zero")
                # Put something more interesting out every ten messages
                log.info("Here's something more interesting")
                log.critical("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                log.critical("Here's a critical message from %s" % name)
                log.debug("hello there")
                log.info("Here's some info from logger %s" % name)
                log.critical("Here's a critical message from %s" % name)

        log_msg_count += 1

    log.warn("%s loggingtest.py log message generator is leaving the party" % name)
    print "%s is done" % name