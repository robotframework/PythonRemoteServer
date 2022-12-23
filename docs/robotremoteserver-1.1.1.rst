==========================
Python Remote Server 1.1.1
==========================

.. default-role:: code

This project implement a generic remote server for `Robot Framework`_ using
Python. Version 1.1.1 fixes compatibility with Python 3.10 and 3.11.

If you have pip_ installed, just run

::

   pip install --upgrade robotremoteserver

to install the latest available release or use

::

   pip install robotremoteserver==1.1.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Remote Server 1.1.1 was released on Friday December 23, 2022.

.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotremoteserver
.. _issue tracker: https://github.com/robotframework/PythonRemoteServer/issues?q=milestone%3Av1.1.1

.. contents::
   :depth: 2
   :local:

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#58`_
      - bug
      - critical
      - Python 3.10 compatibility
    * - `#81`_
      - bug
      - critical
      - Python 3.11 compatibility
    * - `#60`_
      - bug
      - low
      - Misleading documentation related to listening to "all interfaces"

Altogether 3 issues. View on the `issue tracker <https://github.com/robotframework/PythonRemoteServer/issues?q=milestone%3Av1.1.1>`__.

.. _#58: https://github.com/robotframework/PythonRemoteServer/issues/58
.. _#60: https://github.com/robotframework/PythonRemoteServer/issues/60
.. _#81: https://github.com/robotframework/PythonRemoteServer/issues/81
