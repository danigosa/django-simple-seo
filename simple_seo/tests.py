from django.test import TestCase
from django.test.testcases import LiveServerTestCase

from simple_seo.tags import BaseTag
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.ie.webdriver import WebDriver as IEDriver


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
    fixtures = ['fixtures/metadata_fixture.json']

    @classmethod
    def setUpClass(cls):
        cls.firefox = FirefoxDriver()
        cls.chrome = ChromeDriver()
        cls.iexplorer = IEDriver()
        super(FieldPrintingTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.firefox.quit()
        cls.chrome.quit()
        cls.iexplorer.quit()
        super(FieldPrintingTest, cls).tearDownClass()

    def test_title_rendering(self):
        self.firefox.get('%s%s' % (self.live_server_url, '/test/'))
        self.firefox.find_element_by_tag_name('head')



