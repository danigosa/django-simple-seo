from django.test import TestCase
from django.test.testcases import LiveServerTestCase

from simple_seo.tags import BaseTag, TitleTag
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
# from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from testapp.models import MyMetadata


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
        self.mymetadata.save()

        self.firefox = FirefoxDriver()
        # self.chrome = ChromeDriver()

    def tearDown(self):
        self.firefox.quit()
        # self.chrome.quit()

    def test_title_firefox_rendering(self):
        self.firefox.get('%s%s' % (self.live_server_url, '/test/'))
        title_element = self.firefox.title
        self.assertIsNotNone(title_element)
        self.assertEqual(title_element, 'Title Test')

    # def test_title_chrome_rendering(self):
    #     self.chrome.get('%s%s' % (self.live_server_url, '/test/'))
    #     title_element = self.chrome.title
    #     self.assertIsNotNone(title_element)
    #     self.assertEqual(title_element, 'Title Test')




