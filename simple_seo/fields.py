from django.db import models
from .tags import TitleTag


class BaseTagField(models.CharField):
    """
    Base Tag behaviour
    """
    description = "A hand of cards (bridge style)"

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['default'] = ""

        super(BaseTagField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return self.to_python(value).tag_value


class TitleTagField(BaseTagField):
    """
    Creates a field for Title Tag
    * Not Null
    * Not Blank
    * Max-length 68
    * VARCHAR(68)
    """
    description = "Field for Storing <title> tag"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 68
        kwargs['blank'] = False
        kwargs['db_index'] = False
        kwargs['null'] = False
        super(TitleTagField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'VARCHAR(%s)' % self.max_length

    def to_python(self, value):
        if isinstance(value, TitleTag):
            return value
        title = super(TitleTagField, self).to_python(value)
        title_tag = TitleTag(**{'value': title})
        return title_tag