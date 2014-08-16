from django import template
from django.core.urlresolvers import resolve
from django.core.cache import cache
from django.utils import translation
from django.conf import settings
import logging
from ..import get_class_for_view

from ..settings import (
    SEO_CACHE_PREFIX,
    SEO_CACHE_TIMEOUT,
    SEO_USE_CACHE,
)

from ..fields import (
    TitleTagField,
    MetaTagField,
    KeywordsTagField,
    URLMetaTagField,
    ImageMetaTagField
)


log = logging.getLogger(__name__)

register = template.Library()


class MetadataNode(template.Node):
    """
    Template Tag node for Metadata
    * gets the view name from request
    * obtains metadata model and object
    * print each supported field
    """

    @staticmethod
    def _build_prefix(context, view_name):
        lang = translation.get_language()
        return SEO_CACHE_PREFIX + ':' + view_name + ':' + lang + ':' + context['request'].path

    @staticmethod
    def _check_field_i18n(field):
        """
        Avoid fields that has _XX lang prefix
        """
        if not getattr(settings, 'USE_I18N', None) or field is None:
            return False
        for lang in settings.LANGUAGES:
            if '_'+lang[0] in field.name:
                return True

        return False

    def render(self, context):
        view_name = resolve(context['request'].path).url_name  # resolve view name

        # Check if metadata is in cache
        if SEO_USE_CACHE:
            metadata_html = cache.get(self._build_prefix(context, view_name))
            if metadata_html:
                log.debug("Cache metadata hit for view %s" % view_name)
                return metadata_html

        seo_model = get_class_for_view(view_name)
        try:
            metadata = seo_model.objects.get(view_name=view_name)
            metadata_html = ""
            for field in metadata._meta.fields:
                if not self._check_field_i18n(field) and isinstance(
                        field,
                        (TitleTagField, MetaTagField, KeywordsTagField, URLMetaTagField, ImageMetaTagField)):
                    printed_tag = field.to_python(getattr(metadata, field.name)).print_tag()
                    if printed_tag and printed_tag != "":
                        metadata_html += printed_tag + "\n"
                else:
                    pass
            if metadata_html != "" and SEO_USE_CACHE:
                cache.set(self._build_prefix(context, view_name), metadata_html, SEO_CACHE_TIMEOUT)

            if metadata_html:
                return metadata_html
            else:
                return ""
        except seo_model.DoesNotExist as exc:
            # Skipping error to avoid breaking the view
            log.debug("No metadata found for view %s" % view_name)
            return ""


@register.tag
def view_metadata(context, parser):
    return MetadataNode()

