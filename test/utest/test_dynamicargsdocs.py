import unittest

from robotremoteserver import RemoteLibraryFactory


class OwnArgsAndDocs(object):

    def get_keyword_names(self):
        return ['keyword']

    def run_keyword(self, name, args, kwargs=None):
        pass

    def get_keyword_arguments(self, name):
        return ['a1', 'a2=%s' % name, '*args', '**kwargs']

    def get_keyword_documentation(self, name):
        return 'The doc for %s' % name


class OwnArgsAndDocsWithCamelCaseNames(object):

    def getKeywordNames(self):
        return ['keyword']

    def runKeyword(self, name, args):
        pass

    def getKeywordArguments(self, name):
        return ['a1', 'a2=%s' % name, '*args', '**kwargs']

    def getKeywordDocumentation(self, name):
        return 'The doc for %s' % name


class NoArgsOrDocs(object):

    def get_keyword_names(self):
        return ['keyword']

    def run_keyword(self, name, args, kwargs=None):
        pass


class NoArgsOrDocsWithoutKwargs(object):

    def get_keyword_names(self):
        return ['keyword']

    def run_keyword(self, name, args):
        pass


class TestOwnArgsAndDocs(unittest.TestCase):

    def setUp(self):
        self.lib = RemoteLibraryFactory(OwnArgsAndDocs())

    def test_arguments(self):
        self.assertEqual(self.lib.get_keyword_arguments('keyword'),
                         ['a1', 'a2=keyword', '*args', '**kwargs'])

    def test_documentation(self):
        self.assertEqual(self.lib.get_keyword_documentation('keyword'),
                         'The doc for keyword')


class TestOwnArgsAndDocsWithCamelCaseNames(TestOwnArgsAndDocs):

    def setUp(self):
        self.lib = RemoteLibraryFactory(OwnArgsAndDocsWithCamelCaseNames())


class TestNoArgsOrDocs(unittest.TestCase):

    def setUp(self):
        self.lib = RemoteLibraryFactory(NoArgsOrDocs())

    def test_arguments(self):
        self.assertEqual(self.lib.get_keyword_arguments('keyword'),
                         ['*varargs', '**kwargs'])

    def test_documentation(self):
        self.assertEqual(self.lib.get_keyword_documentation('keyword'), '')


class TestNoArgsOrDocsWithoutKwargs(unittest.TestCase):

    def setUp(self):
        self.lib = RemoteLibraryFactory(NoArgsOrDocsWithoutKwargs())

    def test_arguments(self):
        self.assertEqual(self.lib.get_keyword_arguments('keyword'),
                         ['*varargs'])


if __name__ == '__main__':
    unittest.main()
