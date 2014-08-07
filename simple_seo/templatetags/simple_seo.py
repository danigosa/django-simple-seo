from django import template
from django.core.urlresolvers import resolve
from django.core.cache import cache
import logging

from .. import SEO_CACHE_PREFIX, SEO_CACHE_TIMEOUT, SEO_USE_CACHE, get_model_for_view
from ..fields import (
    TitleTagField,
    MetaTagField,
    KeywordsTagField
)


log = logging.getLogger(__name__)

register = template.Library()


def _build_prefix(context, view_name):
    return SEO_CACHE_PREFIX + ':' + view_name + ':' + context['request'].path


class MetadataNode(template.Node):
    """
    Template Tag node for Metadata
    * gets the view name from request
    * obtains metadata model and object
    * print each supported field
    """

    def render(self, context):
        view_name = resolve(context['request'].path).url_name  # resolve view name

        # Check if metadata is in cache
        if SEO_USE_CACHE:
            metadata_html = cache.get(_build_prefix(context, view_name))
            if metadata_html:
                return metadata_html

        seo_model = get_model_for_view(view_name)
        try:
            metadata = seo_model.objects.get(view_name=view_name)
            metadata_html = ""
            for field in metadata._meta.fields:
                if isinstance(field, (TitleTagField, MetaTagField, KeywordsTagField)):
                    metadata_html += field.to_python(getattr(metadata, field.name)).print_tag() + "\n"
                else:
                    pass
            if metadata_html != "" and SEO_USE_CACHE:
                cache.set(_build_prefix(context, view_name), metadata_html, SEO_CACHE_TIMEOUT)

            return metadata_html
        except seo_model.DoesNotExist as exc:
            # Skipping error to avoid breaking the view
            log.exception("No metadata found for view %s" % view_name)


@register.tag
def view_metadata(context, parser):
    return MetadataNode()

