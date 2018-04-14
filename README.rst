Python Remote Server for Robot Framework
========================================

`Robot Framework`_ remote servers allow hosting test libraries on different
processes or machines than Robot Framework itself is running on. This project
implements a generic remote server using the Python_ programming language.
See the `remote library interface documentation`_ for more information about
the remote interface in general as well as for a list of remote server
implementations in other programming languages.

This project is hosted on GitHub_ and downloads are available on PyPI_.

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

Starting from the remote server version 1.1, Robot Framework's `static,
hybrid and dynamic library APIs`__ are all supported. This includes setting
custom name and tags for keywords using the `robot.api.deco.keyword`__
decorator, although the support for tags requires using Robot Framework 3.0.2
or newer. Earlier remote server versions support only the static and hybrid
APIs and do not support the keyword decorator at all.

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
    ``port``                ``8270``          Port to listen. Use ``0`` to select a free port automatically. Can be given as an integer or as a string. The default port ``8270`` is `registered by IANA`__ for remote server usage.
    ``port_file``           ``None``          File to write the port that is used. ``None`` (default) means no such file is written.
    ``allow_stop``          ``'DEPRECATED'``  Deprecated since version 1.1. Use ``allow_remote_stop`` instead.
    ``serve``               ``True``          If ``True``, start the server automatically and wait for it to be stopped. If ``False``, server can be started using the ``serve`` method. New in version 1.1.
    ``allow_remote_stop``   ``True``          Allow/disallow stopping the server remotely using ``Stop Remote Server`` keyword and ``stop_remote_server`` XML-RPC method. New in version 1.1.
    =====================  =================  ========================================

__ https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?search=8270

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
    from examplelibrary import ExampleLibrary

    RobotRemoteServer(ExampleLibrary(), host='10.0.0.42', port=0,
                      port_file='/tmp/remote-port.txt')

Starting from version 1.1, the server can be initialized without starting it by
using the argument ``serve=False``. The server can then started afterwards by
calling its ``serve`` method explicitly. This example is functionally
equivalent to the example above:

.. sourcecode:: python

    from robotremoteserver import RobotRemoteServer
    from examplelibrary import ExampleLibrary

    server = RobotRemoteServer(ExampleLibrary(), host='10.0.0.42', port=0,
                               port_file='/tmp/remote-port.txt', serve=False)
    server.serve()

Starting server on background
-----------------------------

The main benefit of separately initializing and starting the server is that
it makes it easier to start the server in a background thread. Servers started
in a thread work exactly like servers running in the main tread except that
`stopping the server`__ gracefully using ``Ctrl-C`` or signals is not
supported automatically. Users must thus register signal handlers separately
if needed.

Also this following example is functionally nearly equivalent to the earlier
examples except. The main difference is that not all same signals are handled.

.. sourcecode:: python

    import signal
    import threading
    from examplelibrary import ExampleLibrary
    from robotremoteserver import RobotRemoteServer

    server = RobotRemoteServer(ExampleLibrary(), port=0, serve=False)
    signal.signal(signal.SIGINT, lambda signum, frame: server.stop())
    server_thread = threading.Thread(target=server.serve)
    server_thread.start()
    while server_thread.is_alive():
        server_thread.join(0.1)

__ `Stopping remote server`_

Getting active server port
--------------------------

If the server uses the default port ``8270`` or some other port is given
explicitly when `configuring the server`__, you obviously know which port
to use when connecting the server. When using the port ``0``, the server
selects a free port automatically, but there are various ways how to find
out the actual port:

- Address and port that are used are printed into the console where the server
  is started.

- If ``port_file`` argument is used, the server writes the port into the
  specified file where other tools can easily read it. Starting from the
  remote server version 1.1, the server removes the port file automatically
  when the server is stopped.

- Starting from the version 1.1, the server has ``activate`` method that can
  be called to activate the server without starting it. This method returns
  the port that the server binds and also sets it available via the attributes
  discussed below.

- A started or actived server instance has ``server_address`` attribute that
  contains the address and the port as a tuple. Starting from the version 1.1
  there is also ``server_port`` attribute that contains just the port as
  an integer.

__ `Remote server configuration`__

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
  Can be disabled with the ``allow_remote_stop=False`` initialization parameter.

- Running ``python -m robotremoteserver stop [uri]`` which uses the
  aforementioned ``stop_remote_server`` XML-RPC function internally.
  Can be disabled with the ``allow_remote_stop=False`` initialization parameter.

- Using the ``stop_remote_server`` function provided by the
  ``robotremoteserver`` module similarly as when `testing is server running`_.
  Uses the ``stop_remote_server`` XML-RPC function internally and
  can be disabled with the ``allow_remote_stop=False`` initialization parameter.

- Calling the ``stop`` method of the running server instance. Mainly useful when
  `running the server on background`__.

__ `Starting server on background`_
__ `Remote server configuration`_
__ `Starting server on background`_

Testing is server running
-------------------------

Starting from the version 1.0.1, the ``robotremoteserver`` module supports
testing is a remote server running. This can be accomplished by running
the module as a script with ``test`` argument and an optional URI::

    $ python -m robotremoteserver test
    Remote server running at http://127.0.0.1:8270.
    $ python -m robotremoteserver test http://10.0.0.42:57347
    No remote server running at http://10.0.0.42:57347.

Starting from the version 1.1, the ``robotremoteserver`` module contains
function ``test_remote_server`` that can be used programmatically:

.. sourcecode:: python

    from robotremoteserver import test_remote_server

    if test_remote_server('http://localhost:8270'):
        print('Remote server running!')

The ``robotremoteserver`` module can be also used to stop a remote server by
using ``stop`` argument on the command line or by using the
``stop_remote_server`` function programmatically. Testing and stopping should
work also with other Robot Framework remote server implementations.

Listing keywords and viewing documentation
------------------------------------------

Using the built-in Libdoc__ tool you can list the keywords available on the server::

    $ python -m robot.libdoc Remote::http://127.0.0.1:8270 list 
    Count Items In Directory
    Stop Remote Server
    Strings Should Be Equal

It is also possible to show the documentation on the command line by using
argument ``show``. HTML documentation can be created by providing name of
an output file::

    $ python -m robot.libdoc Remote::http://127.0.0.1:8270 MyLibrary.html
    /path/to/MyLibrary.html
    
__ http://robotframework.org/robotframework/#built-in-tools
    
Example
-------

The remote server project contains an example__ that can be studied and also
executed once the library is installed. You can get the example by cloning
the project on GitHub_, and it is also included in the source distribution
available on PyPI_.

__ https://github.com/robotframework/PythonRemoteServer/tree/master/example
