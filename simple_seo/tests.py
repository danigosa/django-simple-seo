from django.test import TestCase
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from django.test.testcases import LiveServerTestCase

from testapp.models import MyMetadata
from simple_seo.tags import TitleTag, MetaTag, KeywordsTag, BaseTag


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


class FieldPrintingTest(LiveServerTestCase):
    """
    Testing TagFields objects printing functions
    """

    def setUp(self):
        self.mymetadata = MyMetadata()
        self.mymetadata.view_name = 'template_test'
        self.mymetadata.title = TitleTag(tag_value='Title Test')
        self.mymetadata.author = MetaTag(meta_name='author', meta_content='Test Author')
        self.mymetadata.description = MetaTag(meta_name='description', meta_content='Test Description')
        self.mymetadata.keywords = KeywordsTag(meta_name='keywords', meta_content='test, author')
        self.mymetadata.save()

        self.firefox = FirefoxDriver()

    def tearDown(self):
        self.firefox.quit()

    def test_title_rendering(self):
        self.firefox.get('%s%s' % (self.live_server_url, '/test/'))
        title_element = self.firefox.title
        self.assertIsNotNone(title_element)
        self.assertEqual(title_element, 'Title Test')

    def test_metatags_rendering(self):
        self.firefox.get('%s%s' % (self.live_server_url, '/test/'))
        author_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'author\']')
        self.assertIsNotNone(author_element)
        self.assertEqual(author_element.get_attribute('content'), 'Test Author')
        description_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'description\']')
        self.assertIsNotNone(description_element)
        self.assertEqual(description_element.get_attribute('content'), 'Test Description')
        keywords_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'keywords\']')
        self.assertIsNotNone(keywords_element)
        self.assertEqual(keywords_element.get_attribute('content'), 'test, author')
