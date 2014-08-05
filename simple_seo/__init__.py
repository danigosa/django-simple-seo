"""
Load settings
"""
from django.conf import settings
from django.utils.six import iteritems

from simple_seo.models import BaseMetadata


SEO_CACHE_PREFIX = getattr(settings, 'SEO_CACHE_PREFIX', 'simple_seo:')
SEO_CACHE_TIMEOUT = getattr(settings, 'SEO_CACHE_PREFIX', 60 * 60 * 24)
SEO_USE_CACHE = getattr(settings, 'SEO_CACHE_PREFIX', False)

_simple_seo_registry = []


def register(model, views=None):
    """
    Registers model for the given views. If no views given then all views are bound.
    If more than one seo model is registered, order matter (in case view name is defined in more than one model,
    first registered is applied only
    :param model: Model to register
    :param views: list of str
    :return:
    """
    if not issubclass(model, BaseMetadata):
        raise TypeError("Model must be an instance of simple_seo.models.BaseMetadata")

    global _simple_seo_registry
    if views and not isinstance(views, (str, list, tuple)):
        raise TypeError("Views must be of type of (str, list, tuple). I.e. 'myview', ('view1', 'view2), ['v1', 'v2']")
    if not views or not len(views):
        views = 'ALL'
    _simple_seo_registry.append(
        {
            model: views
        }
    )


def get_model_for_view(view):
    """
    Given a view name, give a valid seo model. It's gonna be the first model who contains the view name or has
     all-views scope
    :param view:
    :return: model
    """
    if not view:
        raise ValueError("View must have value")

    global _simple_seo_registry
    for registry_dict in _simple_seo_registry:
        for key, value in iteritems(registry_dict):
            if isinstance(value, (list, tuple)):
                if view in value:
                    return key
            elif isinstance(value, str) and value == 'ALL':
                return key
    raise ValueError("No model has been found for view with name %s. Have you registered one?" % view)