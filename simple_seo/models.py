from django.db import models
from .fields import TitleTagField


class BaseMetadata(models.Model):
    """
    Abstract Class
    """
    view_name = models.CharField(max_length=250, null=False, blank=False, choices=(), unique=True, db_index=True)
    title = TitleTagField()
    # keywords = seo.KeywordTag()
    # description = seo.MetaTag(max_length=155)
    # author = seo.Tag('link', head=True)

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