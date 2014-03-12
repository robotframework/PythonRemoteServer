Python Remote Server for Robot Framework
========================================

Introduction
------------

`Robot Framework`_ remote servers allow hosting test libraries on different
processes or machines than Robot Framework itself is running on. This version
is implemented in Python_ and supports also Jython_ (JVM) and
IronPython_ (.NET). See `remote library interface documentation`_ for more
information about the remote interface in general as well as for a list of
remote server implementations in other programming languages.

This project is hosted in GitHub_ and downloads are available in PyPI_.

.. _Robot Framework: http://robotframework.org
.. _Python: http://python.org
.. _Jython: http://jython.org
.. _IronPython: http://ironpython.codeplex.com
.. _remote library interface documentation: http://code.google.com/p/robotframework/wiki/RemoteLibrary
.. _GitHub: https://github.com/robotframework/PythonRemoteServer
.. _PyPI: http://pypi.python.org/pypi/robotremoteserver

Supported Python versions
-------------------------

As already mentioned, this remote server officially supports Python_, Jython_,
and IronPython_, but it should work also with PyPY_. The server has been tested
on Linux, OSX, and Windows, but should work also on other operating systems.

Remote server 1.0 series ought to support all Python, Jython, and IronPython
versions between 2.2 and 2.7, but not all combinations have been thoroughly
tested. Support for versions prior and possibly including 2.5 will likely
be dropped in the future when we target Python 3 compatibility.

.. _PyPy: http://pypy.org/

Installation
------------

The easiest installation approach is using `pip`_:

.. sourcecode:: bash

    $ pip install robotremoteserver

Alternatively you can download the `source distribution`_, extract it, and
install it using:

.. sourcecode:: bash

    $ python setup.py install

Change ``python`` above to ``jython`` or ``ipy`` to install using Jython
or IronPython, respectively, instead of Python.

.. _`pip`: http://www.pip-installer.org
.. _`source distribution`: PyPI_

Starting
--------

The remote server can be started by simply creating an instance of the server
and passing a test library instance or module to it:

.. sourcecode:: python

    from robotremoteserver import RobotRemoteServer
    from mylibrary import MyLibrary

    RobotRemoteServer(MyLibrary())

By default the server listens to address 127.0.0.1 and port 8270. See the next
section for information about configuring the server.

Configuration
-------------

The remote server accepts following configuration parameters:

    ==============  ================  ========================================
       Argument         Default                    Explanation
    ==============  ================  ========================================
    ``library``                       Test library instance or module to host. Mandatory argument.
    ``host``         ``'127.0.0.1'``  Address to listen. Use ``'0.0.0.0'`` to listen to all available interfaces.
    ``port``         ``8270``         Port to listen. Use ``0`` to select a free port automatically.
    ``port_file``    ``None``         File to write port that is used. ``None`` means file is not written.
    ``allow_stop``   ``True``         Allow/disallow stopping the server using ``Stop Remote Server`` keyword.
    ==============  ================  ========================================

Address and port that are used are printed to the console where the server is
started. Writing port to a file by using ``port_file`` argument is especially
useful when the server selects a free port automatically. Other tools can then
easily read the active port from the file. If the file is removed prior to
starting the server, tools can also wait until the file exists to know that
the server is up and running.

Example:

.. sourcecode:: python

    from robotremoteserver import RobotRemoteServer
    from mylibrary import MyLibrary

    RobotRemoteServer(MyLibrary(), host='10.0.0.42', port=0,
                      port_file='/tmp/remote-port.txt', allow_stop=False)

Testing is server running
-------------------------

Starting from version 1.0.1 , ``robotremoteserver`` module supports testing is
a remote server running. This can be accomplished by running the module as
a script with ``test`` argument and an optional URI:

.. sourcecode:: bash

    $ python -m robotremoteserver test
    Remote server running at http://127.0.0.1:8270.
    $ python -m robotremoteserver test http://10.0.0.42:57347
    No remote server running at http://10.0.0.42:57347.

.. tip:: As discussed below, using ``stop`` instead of ``test`` allows stopping
         the server. Both testing and stopping works also against other Robot
         Framework remote server implementations.

Stopping
--------

The remote server can be gracefully stopped using three different methods:

- Hitting ``Ctrl-C`` on the console where the server is running. Starting from
  version 1.0.1 this ought to work regardless the operating system and Python
  interpreter. Python 2.5 and Jython 2.5 on Windows are known exceptions, though.

- Sending the process ``SIGINT``, ``SIGTERM``, or ``SIGHUP`` signal. Does not
  work on Windows. Notice that with Jython you need to send the signal to the
  started Java process, not to the shell typically started by ``jython`` command.

- Using ``Stop Remote Server`` keyword. This can be disabled by using
  ``allow_stop=False`` when starting the server.

- Running ``python -m robotremoteserver stop [uri]`` similarly as when `testing
  is server running`_. Also this can be disabled using ``allow_stop=False``.
  New in version 1.0.1.

Example
-------

The remote server project contains an `example`_ that can be studied and also
executed once the library is installed. The example is also included in the
`source distribution`_.

.. _example: https://github.com/robotframework/PythonRemoteServer/tree/master/example
