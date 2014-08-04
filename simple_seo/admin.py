from __future__ import print_function
from django.contrib.admin import ModelAdmin
from django import forms

from simple_seo.utils import load_view_names


class BaseMetadataForm(forms.ModelForm):
    view_name = forms.ChoiceField(choices=load_view_names())


class BaseMetadataAdmin(ModelAdmin):
    """
    Overrides default admin to add autodiscovered views into a choice field
    """
    list_display = ['view_name', 'title']
    exclude = []
    form = BaseMetadataForm