Remote server example
=====================

This directory contains a very simple remote library example in
`<examplelibrary.py>`__ file and tests using it in `<tests.robot>`__
file. The example library can be executed with Python (both 2 and 3), Jython,
IronPython or PyPy. Also tests can be run with any of these interpreters,
independently from the interpreter used for executing the library.

A precondition to running the example is installing the remote server or
putting it into ``PYTHONPATH`` or equivalent otherwise. After that the remote
library can be started from the command line by just executing it with
the selected interpreter::

    python examplelibrary.py     # Start library on Python
    jython examplelibrary.py     # Start library on Jython

Depending on the operating system configuration, it may also be possible to
simply double-click the library on a file manager.

After the library is running, tests can be executed normally::

    robot tests.robot            # Execute with the `robot` command
    pypy -m robot tests.robot    # Execute `robot` module using PyPy

By default the library starts to listen on connections from the localhost on
port 8270. Both the address and the port to listen to can be configured with
command line arguments to the library, and also given as variables to tests
that are run::

    python examplelibrary.py 192.168.1.15 7777
    robot --variable ADDRESS:192.168.1.15 --variable PORT:7777 tests.robot

Although the remote server in general can be used from a different machine,
this example only works correctly when tests are run on the same machine
where the server is running.

See the example library and tests themselves for details how configuration
is implemented and the general `remote server documentation <../README.rst>`__
for more information about configuring the remote server in general.
