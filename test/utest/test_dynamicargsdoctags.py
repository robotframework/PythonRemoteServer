import unittest

from robotremoteserver import RemoteLibraryFactory


class OwnArgsDocTags(object):

    def get_keyword_names(self):
        return ['keyword']

    def run_keyword(self, name, args, kwargs=None):
        pass

    def get_keyword_arguments(self, name):
        return ['a1', 'a2=%s' % name, '*args', '**kwargs']

    def get_keyword_documentation(self, name):
        return 'The doc for %s' % name

    def get_keyword_tags(self, name):
        return [name, 'tags']


class OwnArgsDocTagsWithCamelCaseNames(object):

    def getKeywordNames(self):
        return ['keyword']

    def runKeyword(self, name, args):
        pass

    def getKeywordArguments(self, name):
        return ['a1', 'a2=%s' % name, '*args', '**kwargs']

    def getKeywordDocumentation(self, name):
        return 'The doc for %s' % name

    def getKeywordTags(self, name):
        return [name, 'tags']


class NoArgsDocTags(object):

    def get_keyword_names(self):
        return ['keyword']

    def run_keyword(self, name, args, *, kwargs=None):
        pass


class NoArgsDocTagsWithoutKwargs(object):

    def get_keyword_names(self):
        return ['keyword']

    def run_keyword(self, name, args):
        pass


class TestOwnArgsDocTags(unittest.TestCase):

    def setUp(self):
        self.lib = RemoteLibraryFactory(OwnArgsDocTags())

    def test_arguments(self):
        self.assertEqual(self.lib.get_keyword_arguments('keyword'),
                         ['a1', 'a2=keyword', '*args', '**kwargs'])

    def test_documentation(self):
        self.assertEqual(self.lib.get_keyword_documentation('keyword'),
                         'The doc for keyword')

    def test_tags(self):
        self.assertEqual(self.lib.get_keyword_tags('keyword'),
                         ['keyword', 'tags'])


class TestOwnArgsDocTagsWithCamelCaseNames(TestOwnArgsDocTags):

    def setUp(self):
        self.lib = RemoteLibraryFactory(OwnArgsDocTagsWithCamelCaseNames())


class TestNoArgsDocTags(unittest.TestCase):

    def setUp(self):
        self.lib = RemoteLibraryFactory(NoArgsDocTags())

    def test_arguments_with_kwargs(self):
        self.assertEqual(self.lib.get_keyword_arguments('keyword'),
                         ['*varargs', '**kwargs'])

    def test_arguments_without_kwargs(self):
        self.lib = RemoteLibraryFactory(NoArgsDocTagsWithoutKwargs())
        self.assertEqual(self.lib.get_keyword_arguments('keyword'),
                         ['*varargs'])

    def test_documentation(self):
        self.assertEqual(self.lib.get_keyword_documentation('keyword'), '')

    def test_tags(self):
        self.assertEqual(self.lib.get_keyword_tags('keyword'), [])


if __name__ == '__main__':
    unittest.main()
