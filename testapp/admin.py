from simple_seo.admin import BaseMetadataAdmin
from django.contrib import admin
from .models import MyMetadata


class MyMetadataAdmin(BaseMetadataAdmin):
    pass

admin.site.register(MyMetadata, MyMetadataAdmin)