import unittest

from KeywordDecorator import KeywordDecorator

from test_robotremoteserver import NonServingRemoteServer


class TestTags(unittest.TestCase):

    def setUp(self):
        self.server = NonServingRemoteServer(KeywordDecorator())

    def test_tags(self):
        self._assert_tags_and_doc('tags', ['tag1', 'tag2'], '')

    def test_tags_with_doc(self):
        self._assert_tags_and_doc('Tags with doc (and custom name)',
                                  ['tag1'], 'Keyword documentation.')

    def _assert_tags_and_doc(self, name, tags, doc):
        self.assertEqual(self.server.get_keyword_tags(name), tags)
        self.assertEqual(self.server.get_keyword_documentation(name), doc)


if __name__ == '__main__':
    unittest.main()
