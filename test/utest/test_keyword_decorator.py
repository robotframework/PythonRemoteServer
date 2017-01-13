import unittest

from KeywordDecorator import KeywordDecorator

from test_robotremoteserver import NonServingRemoteServer


class TestTags(unittest.TestCase):

    def setUp(self):
        self.server = NonServingRemoteServer(KeywordDecorator())

    def test_tags(self):
        self._assert_keyword_doc('tags', 'Tags: tag1, tag2')

    def test_tags_with_doc(self):
        self._assert_keyword_doc('Tags with doc (and custom name)',
                                 'Keyword documentation.\n\nTags: tag1')

    def _assert_keyword_doc(self, name, expected):
        doc = self.server.get_keyword_documentation(name)
        self.assertEqual(doc, expected)


if __name__ == '__main__':
    unittest.main()
