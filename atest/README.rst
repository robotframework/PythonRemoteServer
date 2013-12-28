Acceptance tests for Python Remote Server
=========================================

Tests are executed with `<run.py>`__ script. Run it with ``--help`` or see
its source to view the usage. Actual test cases and test libraries used by
them are in `<tests>`__ and `<libs>`__ directories, respectively.

Running tests requires having both `Robot Framework`__ and
`robotstatuschecker`__ installed. Running ``pip install robotstatuschecker``
ought to take care of installing both. Tests related to binary data require
Robot Framework 2.8.4 or newer.

__ http://robotframework.org
__ https://pypi.python.org/pypi/robotstatuschecker
