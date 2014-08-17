from django.test import TestCase
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from django.test.testcases import LiveServerTestCase
from simple_seo.models import TestMetadata

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
        self.mymetadata = TestMetadata()
        self.mymetadata.view_name = 'template_test'
        self.mymetadata.title = TitleTag(tag_value='Title Test')
        self.mymetadata.author = MetaTag(meta_name='author', meta_content='Test Author')
        self.mymetadata.description = MetaTag(meta_name='description', meta_content='Test Description')
        self.mymetadata.keywords = KeywordsTag(meta_name='keywords', meta_content='test, author')
        # Attr name and class attribute name are not equals, let's do it by setattr
        setattr(self.mymetadata, 'og:title', MetaTag(meta_name='og:title'))
        setattr(self.mymetadata, 'twitter:title', MetaTag(meta_name='twitter:title'))
        setattr(self.mymetadata, 'og:description', MetaTag(meta_name='og:description'))
        setattr(self.mymetadata, 'twitter:description', MetaTag(meta_name='twitter:description'))
        setattr(self.mymetadata, 'og:url', MetaTag(meta_name='og:url', meta_content='http://infantium.com'))
        setattr(self.mymetadata, 'twitter:url', MetaTag(meta_name='twitter:url'))
        setattr(self.mymetadata, 'og:type', MetaTag(meta_name='og:type', meta_content='type'))
        setattr(self.mymetadata, 'twitter:card', MetaTag(meta_name='twitter:card', meta_content='card'))
        setattr(self.mymetadata, 'og:image', MetaTag(meta_name='og:image', meta_content='//infantiumweblog.s3.amazonaws.com/img/partners/animation2/base.png'))
        setattr(self.mymetadata, 'twitter:image', MetaTag(meta_name='twitter:image'))

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

        og_title_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'og:title\']')
        self.assertIsNotNone(og_title_element)
        self.assertEqual(og_title_element.get_attribute('content'), self.firefox.title)  # Should be equal to titleTag
        twitter_title_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'twitter:title\']')
        self.assertIsNotNone(twitter_title_element)
        self.assertEqual(twitter_title_element.get_attribute('content'), og_title_element.get_attribute('content'))

        og_description_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'og:description\']')
        self.assertIsNotNone(og_description_element)
        self.assertEqual(og_description_element.get_attribute('content'), description_element.get_attribute('content'))
        twitter_description_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'twitter:description\']')
        self.assertIsNotNone(twitter_description_element)
        self.assertEqual(twitter_description_element.get_attribute('content'), og_description_element.get_attribute('content'))

        og_url_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'og:url\']')
        self.assertIsNotNone(og_url_element)
        self.assertEqual(og_url_element.get_attribute('content'), 'http://infantium.com')
        twitter_url_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'twitter:url\']')
        self.assertIsNotNone(twitter_url_element)
        self.assertEqual(twitter_url_element.get_attribute('content'), og_url_element.get_attribute('content'))

        og_image_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'og:image\']')
        self.assertIsNotNone(og_image_element)
        self.assertEqual(og_image_element.get_attribute('content'), '//infantiumweblog.s3.amazonaws.com/img/partners/animation2/base.png')
        twitter_image_element = self.firefox.find_element_by_xpath('/html/head/meta[@name=\'twitter:image\']')
        self.assertIsNotNone(twitter_image_element)
        self.assertEqual(twitter_image_element.get_attribute('content'), og_image_element.get_attribute('content'))