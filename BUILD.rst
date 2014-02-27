Releasing remote server
=======================

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
