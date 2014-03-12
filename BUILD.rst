Releasing remote server
=======================

0. Run tests on different operating systems and with different interpreters::

      python test/run.py python
      python test/run.py jython    # use jython.bat on windows
      python test/run.py ipy       # some tests fail due to unicode/str issues

   Above commands run both unit and acceptance tests. See `<test/README.rst>`__
   for more details.

   Unfortunately the test system does not support testing using Jython 2.2.
   We will likely drop support for it in the future, but before that it can
   be tested by running the `example <example/README.rst>`__ using it.

1. Set ``$VERSION`` shell variable to ease copy-pasting further commands::

      VERSION=x.y

2. Update ``__version__`` in `<src/robotremoteserver.py>`__::

      # Linux (GNU sed):
      sed -i "s/__version__ = .*/__version__ = '$VERSION'/" src/robotremoteserver.py
      # OS X (BSD sed):
      sed -i "" "s/__version__ = .*/__version__ = '$VERSION'/" src/robotremoteserver.py
      # Verify changes and commit:
      git diff
      git commit -m "Updated __version__ to $VERSION" src/robotremoteserver.py && git push

3. Tag::

      git tag -a $VERSION -m "Release $VERSION" && git push --tags

4. Create distribution::

      python setup.py sdist register upload

5. Verify that `PyPI page <https://pypi.python.org/pypi/robotremoteserver>`__
   looks good.

6. Test that installation works::

      pip install robotremoteserver --upgrade

7. ``__version__`` back to devel::

      # Linux (GNU sed):
      sed -i "s/__version__ = .*/__version__ = 'devel'/" src/robotremoteserver.py
      # OSX (BSD sed):
      sed -i "" "s/__version__ = .*/__version__ = 'devel'/" src/robotremoteserver.py
      # Verify changes and commit:
      git diff
      git commit -m "__version__ back to devel" src/robotremoteserver.py && git push

8. Advertise on `Twitter <https://twitter.com/robotframework>`__ and on mailing
   lists as needed.
