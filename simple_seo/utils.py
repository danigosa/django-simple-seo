from __future__ import print_function
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
import logging
from django.conf import settings

log = logging.getLogger(__name__)


def _load_pattern(views, pattern, namespace=None):
    """
    Computes RegexURLPattern
    :param pattern: RegexURLPattern
    :param namespace: str
    :return: tuple
    """
    name = getattr(pattern, 'name', None)
    if name:
        if namespace:
            views.append((namespace + ':' + name, namespace + ':' + name))
        else:
            views.append((name, name))


def _load_patterns(views, patterns, namespace=None):
    """
    Computes RegexURLResolver
    :param views: list
    :param patterns: RegexURLResolver
    :param namespace: str
    :return:
    """
    for pattern in patterns:
        if isinstance(pattern, RegexURLPattern):
            _load_pattern(views, pattern, namespace)
        elif isinstance(pattern, RegexURLResolver):
            if namespace and hasattr(pattern, 'namespace') and getattr(pattern, 'namespace'):
                namespace += ':' + pattern.namespace
            elif hasattr(pattern, 'namespace') and getattr(pattern, 'namespace'):
                namespace = pattern.namespace
            _load_patterns(views, pattern.url_patterns, namespace)
        else:
            pass


def load_view_names(urlconf=None):
    """
    Loads view names
    Warning: Only named views are loaded
    :return: generator
    """
    if not urlconf:
        try:
            urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        except Exception as e:
            raise ImproperlyConfigured("Error occurred while trying to load %s: %s"
                                       % (settings.ROOT_URLCONF, str(e)))
    views = []
    for p in urlconf.urlpatterns:
        if isinstance(p, RegexURLPattern):
            _load_pattern(views, p)
        elif isinstance(p, RegexURLResolver):
            _load_patterns(views, p.url_patterns, getattr(p, 'namespace', None))
        else:
            pass

    return views




