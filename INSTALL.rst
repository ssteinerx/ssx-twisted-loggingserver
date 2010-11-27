Installation
------------

Installation should be as easy as getting the repository with:

    # git clone git@github.com:ssteinerx/ssx-twisted-loggingserver.git
    # cd ssx-twisted-loggingserver
    # python setup.py install

Standard warnings about appropriate privileges apply.

Then, assuming you have twisted properly installed:

    # twistd loggingserver --help

Should get you usage information.

I have provided an init.d script that should go in /etc/init.d, and set to be
executable with:

    # chmod +x /etc/init.d/loggingserver

