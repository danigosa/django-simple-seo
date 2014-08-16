from __future__ import print_function
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.loading import get_model
from django.utils.six import iteritems

SEO_MODEL_REGISTRY = getattr(settings, 'SEO_MODEL_REGISTRY', None)
if SEO_MODEL_REGISTRY is None:
    raise ImproperlyConfigured(
        "You must define SEO_MODEL_REGISTRY setting. Look at the documentation here http://bit.ly/1pmE8vU"
    )

SEO_CACHE_PREFIX = getattr(settings, 'SEO_CACHE_PREFIX', 'simple_seo:')
SEO_CACHE_TIMEOUT = getattr(settings, 'SEO_CACHE_PREFIX', 60 * 60 * 24)
SEO_USE_CACHE = getattr(settings, 'SEO_USE_CACHE', False)

_simple_seo_registry = []


def _register(model_name, views_related):
    """
    Registers model for the given views. If no views given then all views are bound.
    If more than one seo model is registered, order matter (in case view name is defined in more than one model,
    first registered is applied only
    :param model: Model to register
    :param views: list of str
    :return:
    """
    if views_related and isinstance(views_related, str):
        if views_related != 'ALL':
            raise ImproperlyConfigured(
                "You must define a list/tuple of view names or 'ALL' in SEO_MODEL_REGISTRY. http://bit.ly/1pmE8vU")
    elif not views_related or not isinstance(views_related, (list, tuple)):
        raise ImproperlyConfigured(
            "You must define a list/tuple of view names or 'ALL' in SEO_MODEL_REGISTRY. http://bit.ly/1pmE8vU")
    _simple_seo_registry.append(
        {
            model_name: views_related
        }
    )


def _get_class_from_name(model_name):
    """
    Returns the Model
    :param model_name: 'app_label.ModelName'
    :return:
    """
    _app_label, _model_name = registry[0].split('.')
    return get_model(_app_label, _model_name)


def get_class_for_view(view):
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
                    return _get_class_from_name(key)
            elif isinstance(value, str) and value == 'ALL':
                return _get_class_from_name(key)
    raise ValueError("No model has been found for view with name %s. Have you registered one?" % view)


def get_classes_for_population():
    """
    Returns classes within the registry
    :return:
    """
    global _simple_seo_registry
    print(_simple_seo_registry)
    for registry_dict in _simple_seo_registry:
        for key, value in iteritems(registry_dict):
            model_klass = _get_class_from_name(key)
            yield model_klass


try:
    for registry in SEO_MODEL_REGISTRY:
        _views_related = registry[1]
        _register(registry[0], _views_related)

except (IndexError, TypeError, ImportError):
    raise ImproperlyConfigured(
        "SEO_MODEL_REGISTRY setting has bad format. Look at the documentation here http://bit.ly/1pmE8vU"
    )