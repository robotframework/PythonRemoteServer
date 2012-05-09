Robot Framework Python Remote Server
====================================

Remote server for `Robot Framework`_ implemented with Python.

Introduction
------------

`Robot Framework`_ is a generic test automation framework implemented
with Python_ that also runs on Jython_ (JVM) and IronPython_
(.NET). Its testing capabilities can be easily extended with generic
and custom test libraries implemented using Python and also Java when
using Jython. It also has a `remote library interface`_ that allows
using test libraries implemented using other languages or running on
different machines.

The `remote library architecture`_ consists of `Remote` test library
that is part of normal Robot Framework installation and separate
language specific remote servers.  This project contains Python_
implementation of the remote server.

.. _Robot Framework: http://robotframework.org>
.. _Python: http://python.org
.. _Jython: http://jython.org
.. _IronPython: TODO
.. _remote library interface:
.. _remote library architecture: TODO


*CONTENT BELOW (AND ALSO ABOVE) WORK-IN-PROGRESS*

Examples Using Remote Servers
-----------------------------

Examples on how test libraries can use the remote servers can be found from
`example` directory. These example libraries can be started with commands::

   python example/examplelibrary.py
   jython example/examplelibrary.py
   ruby example/examplelibrary.rb

Note that all the above commands require that language's module search
path is set so that the respective remote server module can be imported.
By default the servers listen to connections to localhost on port 8270, 
but this can be configured like::

   python example/examplelibrary.py localhost 7777
   ruby example/examplelibrary.rb 192.168.0.1 8270

These examples will start the remote server so that it provides
keywords implemented in the example module. After the remote server is
started, an example test case file can be executed using the familiar
`pybot` or `jybot` commands, possibly giving the port where the server
is listening as a variable::

   pybot example/remote_tests.html
   jybot example/remote_tests.html
   pybot --variable PORT:7777 example/remote_tests.html 

The results should be the same regardless of the example library or start-up
script used.

Testing Remote Servers
----------------------

Tests for the remote servers are inside `test` directory. Acceptance tests
can be executed using `tests/run.py` script and running the script without
arguments provides more information. Notice that tests are not included in 
source distributions.
