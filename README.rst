Python Remote Server for Robot Framework
========================================

`Robot Framework`_ remote servers allow hosting test libraries on different
processes or machines than Robot Framework itself is running on. This project
implements a generic remote server using the Python_ programming language.
See the general `remote library interface documentation`_ for more information
about the remote interface as well as for a list of remote server
implementations in other programming languages.

This project is hosted in GitHub_ and downloads are available in PyPI_.

.. _Robot Framework: http://robotframework.org
.. _remote library interface documentation: https://github.com/robotframework/RemoteInterface
.. _GitHub: https://github.com/robotframework/PythonRemoteServer
.. _PyPI: http://pypi.python.org/pypi/robotremoteserver

.. contents::
   :local:

Supported Python versions
-------------------------

This remote server is implemented with Python_ and supports also Jython_ (JVM),
IronPython_ (.NET) and PyPy_. Remote server version 1.1 and newer support
Python 2.6, 2.7, 3.3, and newer. Remote server 1.0 series supports Python
versions 2.2-2.7.

.. _Python: http://python.org
.. _Jython: http://jython.org
.. _IronPython: http://ironpython.net
.. _PyPy: http://pypy.org/

Supported library APIs
----------------------

Starting from Remote server version 1.1, Robot Framework's standard `static,
hybrid and dynamic library APIs`__ are all supported. This includes setting
custom name and tags for keywords using the `robot.api.deco.keyword`__
decorator. Earlier versions support only the static and hybrid APIs and do
not support the keyword decorator.

For most parts these APIs work exactly like when using with Robot Framework
normally. There main limitation is that logging using ``robot.api.logger`` or
Python's ``logging`` module `is currently not supported`__.

__ http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#creating-test-libraries
__ http://robot-framework.readthedocs.io/en/latest/autodoc/robot.api.html#robot.api.deco.keyword
__ https://github.com/robotframework/PythonRemoteServer/issues/26

Installation
------------

The easiest installation approach is using `pip`_::

    pip install robotremoteserver

Alternatively you can download the source distribution from PyPI_, extract it
and install the remote server using::

    python setup.py install

.. _`pip`: http://www.pip-installer.org

Remote server configuration
---------------------------

The remote server is implemented as a class ``RobotRemoteServer`` and it
accepts the following configuration parameters when it is initialized:

    =====================  =================  ========================================
          Argument              Default                    Explanation
    =====================  =================  ========================================
    ``library``                               Test library instance or module to host. Mandatory argument.
    ``host``                ``'127.0.0.1'``   Address to listen. Use ``'0.0.0.0'`` to listen to all available interfaces.
    ``port``                ``8270``          Port to listen. Use ``0`` to select a free port automatically. Can be given as an integer or as a string.
    ``port_file``           ``None``          File to write the port that is used. ``None`` (default) means no such file is written.
    ``allow_stop``          ``'DEPRECATED'``  DEPRECATED. User ``allow_remote_stop`` instead.
    ``serve``               ``True``          If ``True``, start the server automatically and wait for it to be stopped. If ``False``, server can be started using the ``serve`` method. New in version 1.1.
    ``allow_remote_stop``   ``True``          Allow/disallow stopping the server remotely using ``Stop Remote Server`` keyword and ``stop_remote_server`` XML-RPC method. New in version 1.1.
    =====================  =================  ========================================

Address and port that are used are printed to the console where the server is
started. Writing port to a file by using ``port_file`` argument is especially
useful when the server selects a free port automatically. Other tools can then
easily read the active port from the file. If the file is removed prior to
starting the server, tools can also wait until the file exists to know that
the server is up and running. Starting from version 1.1, the server removes
the port file automatically when it is stopped.

Starting remote server
----------------------

The remote server can be started simply by creating an instance of the server
and passing a test library instance or module to it:

.. sourcecode:: python

    from robotremoteserver import RobotRemoteServer
    from mylibrary import MyLibrary

    RobotRemoteServer(MyLibrary())

By default the server listens to address 127.0.0.1 and port 8270. As `discussed
above`__, the remote server accepts various configuration parameters. Some of
them are used by this example:

__ `Remote server configuration`_

.. sourcecode:: python

    from robotremoteserver import RobotRemoteServer
    from mylibrary import MyLibrary

    RobotRemoteServer(MyLibrary(), host='10.0.0.42', port=0,
                      port_file='/tmp/remote-port.txt')

Starting from version 1.1, the server can be initialized without starting it by
using the argument ``serve=False``. The server can then started afterwards by
calling its ``serve`` method explicitly. This example is functionally
equivalent to the example above:

.. sourcecode:: python

    server = RobotRemoteServer(MyLibrary(), host='10.0.0.42', port=0,
                               port_file='/tmp/remote-port.txt', serve=False)
    server.serve()

Starting server on background
-----------------------------

The main benefit of separately initializing and starting the server is that
it makes it easier to start the server on a background thread. This is
illustrated by the following example:

.. sourcecode:: python

    import threading
    import time

    from robotremoteserver import RobotRemoteServer
    from mylibrary import MyLibrary

    try:
        raw_input
    except NameError:  # Python 3
        raw_input = input

    # Initialize server and start it in a thread.
    server = RobotRemoteServer(MyLibrary(), port=0, serve=False)
    server_thread = threading.Thread(target=server.serve)
    server_thread.start()
    # Wait for server to be activated and port to be bind.
    while server.server_port == 0:
        time.sleep(0.1)
    # Serve requests until user presses enter.
    raw_input('Press enter to stop the server.\n')
    server.stop()
    server_thread.join()

Servers started this way work mostly like servers started on the main thread.
The main difference is that stopping the server gracefully using ``Ctrl-C``
or signals is not supported automatically. The user must register signal
handlers separately if needed.

Stopping remote server
----------------------

The remote server can be gracefully stopped using several different methods:

- Hitting ``Ctrl-C`` on the console where the server is running. Not supported
  automatically if the server is `started on a background thread`__.

- Sending the process ``SIGINT``, ``SIGTERM``, or ``SIGHUP`` signal. Does not
  work on Windows and not supported if the server is started on a background
  thread.

- Using ``Stop Remote Server`` keyword. Can be disabled by using
  ``allow_remote_stop=False`` when `initializing the server`__.

- Using ``stop_remote_server`` function in the XML-RPC interface.
  Can be disabled with ``allow_remote_stop=False``.

- Running ``python -m robotremoteserver stop [uri]`` which uses the
  aforementioned ``stop_remote_server`` XML-RPC function internally.
  Can be disabled with ``allow_remote_stop=False``.

- Using the ``stop_remote_server`` function provided by the
  ``robotremoteserver`` module similarly as when `testing is server running`_.
  Uses the ``stop_remote_server`` XML-RPC function internally and
  can be disabled with ``allow_remote_stop=False``.

- Calling ``stop`` method of the running server instance. Mainly useful when
  `running the server on background`__.

__ `Starting server on background`_
__ `Remote server configuration`_
__ `Starting server on background`_

Testing is server running
-------------------------

Starting from version 1.0.1 , the ``robotremoteserver`` module supports testing
is a remote server running. This can be accomplished by running the module as
a script with ``test`` argument and an optional URI::

    $ python -m robotremoteserver test
    Remote server running at http://127.0.0.1:8270.
    $ python -m robotremoteserver test http://10.0.0.42:57347
    No remote server running at http://10.0.0.42:57347.

Starting from version 1.1, ``robotremoteserver`` module contains function
``test_remote_server`` that can be used programmatically:

.. sourcecode:: python

    from robotremoteserver import test_remote_server

    if test_remote_server('http://localhost:8270'):
        print('Remote server running!')

The ``robotremoteserver`` module can be also used to stop a remote server by
using ``stop`` argument on the command line or by using the
``stop_remote_server`` function programmatically. Testing and stopping should
work also with other Robot Framework remote server implementations.

Example
-------

The remote server project contains an example__ that can be studied and also
executed once the library is installed. You can get the example by cloning
the project on GitHub_, and it is also included in the source distribution
available on PyPI_.

__ https://github.com/robotframework/PythonRemoteServer/tree/master/example
