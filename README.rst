PythonLoggingServer
===================

A Python Logging Server by Doug Farrell
Original at: http://code.google.com/p/python-loggingserver/

Modified by Steve Steiner (ssteinerX@gmail.com)
ssteinerX github: https://github.com/ssteinerx/python-loggingserver

Introduction
------------

This project provides a Python Logging Server based on the Twisted framework.
This creates a centralized logging server to complement the logging module's
SocketHandler client.

Purpose
-------

My (Doug Farrell) reason for creating this is I like the Python logging
system, but wasn't crazy about every Python process on every separate server
having its own log file. Plus, I had to know which log file to look in to find
a problem that might be occurring.

I could have all Python processes point to one log file, but there was nothing
to prevent them from trashing the log file by trying to write at the same
time.

In addition, processes on other servers couldn't do this unless they used some
mounted/shared file system. Plus, tailing a log file, while useful, didn't
have the immediacy I was looking for.

The logging server resolves these issues by providing the following:

* It synchronizes access to the one central log file through the network
  interface
* Because it is network based, multiple Python processes can send log messages
  to it
* Again, because it is network based, multiple Python processes on multiple
  servers can send log messages to it
* It provides a centralized status page that shows
    1. Some statistics on the logging server itself
    2. A color coded, chronological listing of the most recent 300 log
       messages that is updated every 5 seconds.
    3. A separate user configurable CSS file to control the presentation of
       the status page

Requirements
------------

The logging server requires the Twisted framework be installed on your system
in order to run. The easiest way to do this is to use easy_install to install
the Twisted system.

Installation
------------

The logging server isn't a package that is added to a running application, it
is a daemon process that runs stand alone. When run it reads its configuration
file and begins to listen on two network socket ports for messages. On one
port it is listening for log messages that were transmitted by client
programs.

On the other port it is listening for HTTP requests for the status page. For
this reason the project code can be anywhere on the system so long as it can
be run by Twisted. The program will need access to its configuration file.
For a production installation the code should be located in some central
script location.

Status Page
-----------

FIXED: ssteinerX -- the loggingserver.css file is now just served by Twisted
>The loggingserver.css file will need to be accessible to the web based status
>page, you'll see in the default code it's referenced as
>http://lcoalhost/loggingserver.css.

>This means that a web server answering to port 80 will need to have access to
>the file in order to serve it up. For a production system you'll want to put
>this on a web server at a URL you can rely on and change the
>loggingserverwebpage.py file to reflect this.

Running
-------

The logging server is run as a daemon process by Twisted, and is invoked as
follows:

    twistd --pidfile=loggingserver.pid --logfile=loggingserver.log --python=loggingserver.py

This will tell Twisted to start the logging server by running the
loggingserver.py main file. It will save the PID of the process in the
loggingserver.pid file and it will log its own messages to the
loggingserver.log file. These are just an example of how to run the logging
server, modify as need be for your purposes.

The logging server process can be stopped by this line:

    kill `cat loggingserver.pid`

Running as Twistd Plug-in
------------------------------


Testing
-------

Once you have the logging server running as described above, you can test the
system by running the client test application. This is done as follows:

    python loggingtest.py <module name>

Where <module name> is just single string value used by the logging system to
register a module name for logging. This name will show up in the logged
messages.

Once the test is running bring up a web server and browse to
http://localhost:9021, which will take you to the status page, and should be
showing messages as they are coming in from the test application.

You can run as many instances of the test application as you'd like, and
you'll see log messages from all of them appearing in the status window. To
stop the test application hit CTRL-C, which will cause it to exit gracefully.

References
----------

I wrote a more complete article about the logging server that appeared in the
October issue of Python Magazine.


**Comment by e...@sxnet.com.ar, Aug 06, 2009**

Excellent app ... i'm writing a python system monitor using most from psi and
enumprocess, so your app is very usefull for me! Trying it right now :)

**Comment by andresgattinoni, Jan 28, 2010**
Sounds great. Is it possible to integrate the logging server with syslog?

**Comment by hugotruffegm, Feb 01, 2010**

Hello, you could put the note here to read Python Magazine?. Or take an
example because of complications with running the application.

Tutbogears configure an application, which sends a message to the server
(critical level). this message reaches the server log, but the webpage did not
add the server log and did not show anything.

Log Records Total 0

I will be very helpful

Surely I am configuring something wrong

**Comment by ggenellina, Feb 10, 2010**
Based on your code, I wrote a smaller recipe that doesn't require Twisted nor
any other external package, and is fully auto-contained:

    http://code.activestate.com/recipes/577025/

**Comment by project member doug.farrell, Apr 13, 2010**

Hi everyone, A friend pointed out that there are comments here, which I hadn't
seen as they are quite long after the article published. My apologies for not
looking sooner.

I might look at integrating the logging_server with syslog, but at present
it's lower on my priority list than other items to work on.

ggenellina, very nice Twisted free application you wrote. Based on my
experience with Twisted, I think the logging_server is more "bullet proof",
but for those people who don't want to install Twisted, or who can't run it
(Python 3+ users), your solutions is very good.

I'm thinking about making changes to the logging_server, here is what I'm
considering:

* Bring the logging server up to the Twisted 10.0 release.
* Make use of the Twisted plug-in facility to add handlers to the system so
  users could add customer handling, ie: Instant Messaging for instance.
* Add handlers for XMLRPC, JSON and HTTP Form Encode log messages so other
  languages besides Python could talk to the logging_server and make use of it.

I'd like to know what you think, thanks! Doug

**Comment by sstein...@gmail.com, Today (moments ago)**

I just found this and would love to help.

I need this to monitor a cluster of servers with a real-time web display of
log info at various levels, so I'm going to have to serve on multiple ports or
make the filtering part of the web page.

I haven't gotten this running yet, but I'm on Python 2.7 and Twisted 10.1, so
I'll certainly make any necessary changes available to anyone who wants them.

I'm going to fork this at github so I can work on it, my github ID is
ssteinerx as well if anyone wants to follow along there.

S aka/ssteinerX aka/Steve Steiner

**Comment by sstein...@gmail.com, Today (moments ago)**

I have posted fixes for two of the issues in the issue tracker, created a
README.txt from the wiki contents, and am now adding a setup.py.

For my own use, I'm going to have to document how to pull this into a Twisted
app from the installed version, so I'll post that to the wiki on github (i
don't seem to be able to do anything but comment here on google).

I need a WebSocket? based implementation for my monitor, and have that
(WebSocket?, that is)working well in Twisted, so I'll probably throw that in
for fun later.

Anyone who wants to follow or help, or if you'd like to pull my fixes in:

    https://github.com/ssteinerx/python-loggingserver

Thanks,

S
