from __future__ import print_function
from django.db.models.loading import get_model
from django.utils.six import iteritems
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
import logging
from django.conf import settings as django_settings

log = logging.getLogger(__name__)

from .settings import SEO_MODEL_REGISTRY

#  Global registries
_simple_seo_registry = []
_view_names_registry = []


def _register(model_name, views_related):
    """
    Registers model for the given views. If no views given then all views are bound.
    If more than one seo model is registered, order matter (in case view name is defined in more than one model,
    first registered is applied only
    :param model_name: Model to register
    :param views_related: list of str
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


try:
    for registry in SEO_MODEL_REGISTRY:
        _views_related = registry[1]
        _register(registry[0], _views_related)

except (IndexError, TypeError, ImportError):
    raise ImproperlyConfigured(
        "SEO_MODEL_REGISTRY setting has bad format. Look at the documentation here http://bit.ly/1pmE8vU"
    )


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
    global _view_names_registry
    if len(_view_names_registry):
        return _view_names_registry

    if not urlconf:
        try:
            urlconf = __import__(django_settings.ROOT_URLCONF, {}, {}, [''])
        except Exception as ie:
            raise ImproperlyConfigured("Error occurred while trying to load %s: %s"
                                       % (getattr(settings, 'ROOT_URLCONF', '\'NO settings.ROOT_URLCONF found\''), str(ie)))

    views = []
    for p in urlconf.urlpatterns:
        if isinstance(p, RegexURLPattern):
            _load_pattern(views, p)
        elif isinstance(p, RegexURLResolver):
            _load_patterns(views, p.url_patterns, getattr(p, 'namespace', None))
        else:
            pass
    _view_names_registry.extend(views)
    return _view_names_registry




