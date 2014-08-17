from django.contrib import admin
from simple_seo.admin import BaseMetadataAdmin
from .models import MyMetadata


class MyMetadataAdmin(BaseMetadataAdmin):
    pass


admin.site.register(MyMetadata, MyMetadataAdmin)