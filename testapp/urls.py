try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'simple_seo.tests.testapp.views',
    url(r'^test/', 'template_test'),
)