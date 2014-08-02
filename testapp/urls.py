from django.conf.urls import patterns, url, include
from django.contrib import admin
from .views import template_test

urlpatterns = patterns(
    '',
    url(r'^test/', template_test,  name='template_test'),
)

admin.autodiscover()

urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)