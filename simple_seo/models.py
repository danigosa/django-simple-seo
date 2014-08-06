from django.db import models
from .fields import (
    TitleTagField,
    KeywordsTagField,
    MetaTagField,
    ImageMetaTagField,
    URLMetaTagField
)


class BaseMetadata(models.Model):
    """
    Abstract Base Metadata Class
    """
    view_name = models.CharField(max_length=250, null=False, blank=False, choices=(), unique=True, db_index=True)
    title = TitleTagField()
    keywords = KeywordsTagField()
    description = MetaTagField()
    author = MetaTagField()

    class Meta:
        abstract = True


class OpenGraphMetadata(BaseMetadata):
    """
    Abstract Base Metadata Class with Open Graph Tags
    """
    og_title = MetaTagField(name='og:title', max_length=95)
    og_type = MetaTagField(name='og:type', max_length=15)
    og_image = ImageMetaTagField(name='og:image', upload_to='seo/images/')
    og_url = URLMetaTagField(name='og:url')
    og_description = MetaTagField(name='og:description', max_length=297)
    og_admins = MetaTagField(name='og:admins', max_length=297)

    class Meta:
        abstract = True











        # og_title = seo.MetaTag(name='og:title', max_length=95)
        # og_type = seo.MetaTag(name='og:type', max_length=15)
        # og_image = seo.MetaTag(name='og:image', max_length=250)
        # og_url = seo.MetaTag(name='og:url', max_length=250)
        # og_description = seo.MetaTag(name='og:description', max_length=297)
        # og_admins = seo.MetaTag(name='og:admins', max_length=297)
        # twitter_title = seo.MetaTag(name='twitter:title', max_length=70)
        # twitter_card = seo.MetaTag(name='twitter:card', max_length=15)
        # twitter_image = seo.MetaTag(name='twitter:image', max_length=250)
        # twitter_url = seo.MetaTag(name='twitter:url', max_length=250)
        # twitter_description = seo.MetaTag(name='twitter:description', max_length=200)