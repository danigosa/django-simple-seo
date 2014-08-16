from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

SEO_MODEL_REGISTRY = getattr(settings, 'SEO_MODEL_REGISTRY', None)
if SEO_MODEL_REGISTRY is None:
    raise ImproperlyConfigured(
        "You must define SEO_MODEL_REGISTRY setting. Look at the documentation here http://bit.ly/1pmE8vU"
    )

SEO_CACHE_PREFIX = getattr(settings, 'SEO_CACHE_PREFIX', 'simple_seo:')
SEO_CACHE_TIMEOUT = getattr(settings, 'SEO_CACHE_TIMEOUT', 60 * 60 * 24)
SEO_USE_CACHE = getattr(settings, 'SEO_USE_CACHE', False)