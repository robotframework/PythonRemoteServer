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

Installation
------------

The easiest installation approach is using `pip`_:

.. sourcecode:: bash

    $ pip install robotremoteserver

Alternatively you can download the `source distribution`_, extract it, and
install it using:

.. sourcecode:: bash

    $ python setup.py install

.. _`pip`: http://www.pip-installer.org
.. _`source distribution`: PyPI_

Usage
-----

Starting
~~~~~~~~

The remote server can be started by simply creating an instance of the server
and passing a test library instance or module to it:

.. sourcecode:: python

    from robotremoteserver import RobotRemoteServer
    from mylibrary import MyLibrary

    RobotRemoteServer(MyLibrary())

By default the server listens to address 127.0.0.1 and port 8270. See the next
section for information how to configure them.

Configuration
~~~~~~~~~~~~~

The remote server accepts following configuration parameters:

    ==============  ================  ========================================
       Argument        Default                   Explanation
    ==============  ================  ========================================
    ``host``         ``'127.0.0.1'``  Address to listen. Use ``'0.0.0.0'`` to listen to all available interfaces.
    ``port``         ``8270``         Port to listen. Use ``0`` to select free port automatically.
    ``port_file``    ``None``         File to write port that is used.
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

Stopping
~~~~~~~~

The remote server can be gracefully stopped using three different methods:

- Hitting ``Ctrl-C`` on the console where the server is running.
- Sending the process ``SIGINT``, ``SIGTERM``, or ``SIGHUP`` signal.
- Using ``Stop Remote Server`` keyword (unless explicitly disabled).

Example
-------

The remote server project contains an `example`_ that can be studied and also
executed once the library is installed. The example is also included in the
`source distribution`_.

.. _example: https://github.com/robotframework/PythonRemoteServer/tree/master/example
