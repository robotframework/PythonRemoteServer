Remote server example
=====================

This directory contains a very simple remote library example in
`<examplelibrary.py>`__ file and tests using it in `<example_tests.robot>`__.
The example library can be executed with Python, Jython, and IronPython.
Also tests can be run with any of these interpreters, independently from
the interpreter used for executing the library.

A precondition to running the example is installing the remote server or
putting it into PYTHONPATH or equivalent otherwise. After that the remote
library can be started from the command line by just executing it with
the selected interpreter::

    python examplelibrary.py     # Execute on Python
    jython examplelibrary.py     # Execute on Jython
    ipy examplelibrary.py        # Execute on IronPython

Alternatively the library can be double-clicked on a file manager. In that
case it will run on Python.

After the library is running, tests can be executed normally::

    pybot example_tests.robot    # Execute with Python
    jybot example_tests.robot    # Execute with Jython
    ipy example_tests.robot      # Execute with IronPython

It is possible to use custom address and port by passing them as arguments
to the library, which passes them further to the remote server, and overriding
related variables when running tests::

    python examplelibrary.py 0.0.0.0 7777
    pybot --variable PORT:7777 example_tests.py

See the example library and tests themselves for details how configuration
is implemented and the general `remote server documentation <../README.rst>`__
for more information about configuring the remote server in general.
