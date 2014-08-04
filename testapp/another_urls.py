from django.conf.urls import patterns, url

from .views import template_test


urlpatterns = patterns(
    '',
    url(r'^', template_test, name='template_test2'),
)