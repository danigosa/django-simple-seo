"""
Load settings
"""
from django.conf import settings

SEO_CACHE_PREFIX = getattr(settings, 'SEO_CACHE_PREFIX', 'simple_seo:')
SEO_CACHE_TIMEOUT = getattr(settings, 'SEO_CACHE_PREFIX', 60*60*24)
SEO_USE_CACHE = getattr(settings, 'SEO_CACHE_PREFIX', True)
