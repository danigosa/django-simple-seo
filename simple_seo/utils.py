from __future__ import print_function
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import logging

log = logging.getLogger(__name__)


def load_view_names():
    """
    Loads view names
    Warning: Only named views are loaded
    :return: tuple
    """
    try:
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
    except Exception as e:
        raise ImproperlyConfigured("Error occurred while trying to load %s: %s" % (settings.ROOT_URLCONF, str(e)))

    named_views = None
    for view in getattr(settings, 'VIEWS_WITH_NAMESPACE', ()):
        if named_views:
            named_views = (named_views, (view, view))
        else:
            named_views = ((view, view),)

    for pattern in urlconf.urlpatterns:
        name = getattr(pattern, 'name', "")
        if name:
            if named_views:
                named_views = (named_views, (name, name))
            else:
                named_views = ((name, name),)
        else:
            log.debug("Skipping pattern...")

    return named_views