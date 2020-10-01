========================
Python Remote Server 1.1
========================


.. default-role:: code


This project implement a generic remote server for `Robot Framework`_ using
Python. Version 1.1 is a new release with some high priority enhancements
such as support for Python 3 and Robot Framework's dynamic library interface.
There are no changes in this version compared to the earlier released
Python Remote Server 1.1 release candidate 2.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotremoteserver

to install the latest available release or use

::

   pip install robotremoteserver==1.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Remote Server 1.1 was released on Wednesday September 27, 2017.

.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotremoteserver

Its Amazing Project i should make it.


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

The most important enhancement in this release is Python 3 support (`#17`_)
but the support for Robot Framework's dynamic library API (`#18`_) is
very important too.

Other high priority enhancements are the support for starting the server on
background (`#22`_) and possibility to use the `@keyword` decorator (`#35`_).

Acknowledgements
================

User `@epronk <https://github.com/epronk>`_ implemented support for
`@keyword` decorator (`#35`_) and Kevin Ormbrek (`@ombre42
<https://github.com/ombre42>`_) provided initial pull request to support
the dynamic library interface (`#18`_).

Thanks also everyone who has submitted issues, tested the preview releases,
or helped otherwise!

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#17`_
      - enhancement
      - critical
      - Python 3 support
    * - `#18`_
      - enhancement
      - critical
      - Support for dynamic library API
    * - `#22`_
      - enhancement
      - high
      - Support starting server on background
    * - `#35`_
      - enhancement
      - high
      - Support `@keyword` decorator
    * - `#38`_
      - enhancement
      - medium
      - Support `get_keyword_tags` method that was added in RF 3.0.2

Altogether 5 issues. View on the `issue tracker <https://github.com/robotframework/PythonRemoteServer/issues?q=milestone%3Av1.1>`__.

.. _#17: https://github.com/robotframework/PythonRemoteServer/issues/17
.. _#18: https://github.com/robotframework/PythonRemoteServer/issues/18
.. _#22: https://github.com/robotframework/PythonRemoteServer/issues/22
.. _#35: https://github.com/robotframework/PythonRemoteServer/issues/35
.. _#38: https://github.com/robotframework/PythonRemoteServer/issues/38
