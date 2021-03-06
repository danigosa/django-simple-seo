from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import template_test


urlpatterns = patterns(
    '',
    url(r'^test/', template_test, name='template_test'),
    url(r'^test2/', include('testapp.another_urls', namespace='foo', app_name='faa'))

)

admin.autodiscover()

urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    import debug_toolbar
    urlpatterns += patterns(
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
