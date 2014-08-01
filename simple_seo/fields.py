from django.db import models
from django.utils.six import with_metaclass
from .tags import TitleTag


class BaseTagField(models.Field):
    """
    Base Tag behaviour
    """
    description = "A hand of cards (bridge style)"

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['default'] = ""

        super(BaseTagField, self).__init__(*args, **kwargs)


class TitleTagField(with_metaclass(models.SubfieldBase, BaseTagField)):
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

    def db_type(self, connection):
        return 'char(%s)' % self.max_length

    def to_python(self, value):
        if isinstance(value, TitleTag):
            return value

        titleTag = TitleTag(title=value)
        return titleTag