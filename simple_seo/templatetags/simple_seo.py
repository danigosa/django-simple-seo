from django import template
from django.core.urlresolvers import resolve
from simple_seo import SEO_CACHE_PREFIX, SEO_CACHE_TIMEOUT, SEO_USE_CACHE
from django.core.cache import cache

register = template.Library()


class MetadataNode(template.Node):
    """
    Template Tag node for Metadata
    """
    def render(self, context):
        view_name = resolve(context['request'].path).url_name  # resolve view name

        # Check if metadata is in cache
        if SEO_USE_CACHE:
            built_prefix = SEO_CACHE_PREFIX + ':' + view_name + ':' + context['request'].path
            metadata = cache.get(built_prefix)
            if metadata:
                return metadata





@register.tag
def view_metadata(context, parser, token):
    if token:
        raise template.TemplateSyntaxError("'view_metadata' tag does not require any argument")
    return MetadataNode()

