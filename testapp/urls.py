from django.conf.urls import patterns, url, include
from django.contrib import admin

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