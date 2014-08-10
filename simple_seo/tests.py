from django.test import TestCase

from simple_seo.tags import BaseTag


class TagPrintingTest(TestCase):
    """
    Testing Tag objects printing functions
    """
    base_tag_selfclosed = None
    base_tag_notselfclosed = None

    def setUp(self):
        self.base_tag_notselfclosed = BaseTag(tag_name='test', self_closed=False, tag_value='Test Tag',
                                              meta_name='meta name',
                                              meta_content='meta content')
        self.base_tag_selfclosed = BaseTag(tag_name='test', self_closed=True, tag_value='Test Tag',
                                           meta_name='meta name',
                                           meta_content='meta content')

    def tearDown(self):
        self.base_tag_selfclosed = None
        self.base_tag_notselfclosed = None

    def test_notselfclosed_tag(self):
        self.assertEqual(self.base_tag_notselfclosed.print_tag(), '<test>Test Tag</test>')

    def test_selfclosed_tag(self):
        self.assertEqual(self.base_tag_selfclosed.print_tag(), '<test name="meta name" content="meta content" />')


