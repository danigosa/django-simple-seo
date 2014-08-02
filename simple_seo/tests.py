from django.test import TestCase
from simple_seo.tags import TitleTag


class PrintingTest(TestCase):
    def setUp(self):
        self.title_tag = TitleTag(title='test')
