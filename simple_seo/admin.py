from __future__ import print_function
from django.contrib.admin import ModelAdmin
from django import forms

from .import load_view_names


class BaseMetadataForm(forms.ModelForm):
    view_name = forms.ChoiceField(choices=load_view_names())


class BaseMetadataAdmin(ModelAdmin):
    """
    Overrides default admin to add autodiscovered views into a choice field
    """
    list_display = ['view_name', 'title']
    exclude = []
    form = BaseMetadataForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(BaseMetadataAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'title':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        if db_field.name == 'description':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        if db_field.name == 'keywords':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        if db_field.name == 'og:title':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        if db_field.name == 'og:description':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        if db_field.name == 'twitter:title':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        if db_field.name == 'twitter:description':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield