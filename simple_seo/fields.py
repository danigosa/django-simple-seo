from django.db import models
from .tags import TitleTag


class TitleTagField(models.CharField):
    """
    Creates a field for Title Tag
    """
    description = "Field for Storing <title> tag"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 68
        kwargs['blank'] = False
        kwargs['db_index'] = False
        kwargs['null'] = False
        super(TitleTagField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, TitleTag):
            return value
        title = super(TitleTagField, self).to_python(value)
        titleTag = TitleTag(title=title)
        return titleTag