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
    author = MetaTagField(null=True, blank=True)

    class Meta:
        abstract = False


class OpenGraphMetadata(BaseMetadata):
    """
    Abstract Base Metadata Class with Open Graph Tags
    """
    og_title = MetaTagField(name='og:title', max_length=95, null=True, blank=True)
    og_type = MetaTagField(name='og:type', max_length=15, null=True, blank=True)
    og_image = ImageMetaTagField(name='og:image', upload_to='seo/images/', null=True, blank=True)
    og_url = URLMetaTagField(name='og:url', null=True, blank=True)
    og_description = MetaTagField(name='og:description', max_length=297, null=True, blank=True)
    og_admins = MetaTagField(name='og:admins', max_length=297, null=True, blank=True)

    class Meta:
        abstract = False


class TwitterMetadata(BaseMetadata):
    """
    Abstract Base Metadata Class with Twitter Tags
    """
    twitter_title = MetaTagField(name='twitter:title', max_length=70, null=True, blank=True)
    twitter_card = MetaTagField(name='twitter:card', max_length=15, null=True, blank=True)
    twitter_image = ImageMetaTagField(name='twitter:image', upload_to='seo/images/', null=True, blank=True)
    twitter_description = MetaTagField(name='twitter:description', max_length=200, null=True, blank=True)

    class Meta:
        abstract = False


class AllMetadata(OpenGraphMetadata):
    """
    Abstract Base Metadata Class with All Tags
    """
    twitter_title = MetaTagField(name='twitter:title', max_length=70, null=True, blank=True)
    twitter_card = MetaTagField(name='twitter:card', max_length=15, null=True, blank=True)
    twitter_image = ImageMetaTagField(name='twitter:image', upload_to='seo/images/', null=True, blank=True)
    twitter_url = URLMetaTagField(name='twitter:url', null=True, blank=True)
    twitter_description = MetaTagField(name='twitter:description', max_length=200, null=True, blank=True)

    class Meta:
        abstract = False

try:
    # In case South is installed
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        [],
        [
            "^simple_seo\.fields\.TitleTagField",
            "^simple_seo\.fields\.MetaTagField",
            "^simple_seo\.fields\.URLMetaTagField",
            "^simple_seo\.fields\.ImageMetaTagField",
            "^simple_seo\.fields\.KeywordsTagField",
        ])
except ImportError:
    pass