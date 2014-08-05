from django.db import models
from django.utils.six import with_metaclass

from .tags import (
    TitleTag,
    MetaTag,
    KeywordsTag
)


class BaseTagField(with_metaclass(models.SubfieldBase, models.CharField)):
    """
    Base Tag behaviour
    """
    description = "A hand of cards (bridge style)"

    def get_prep_value(self, value):
        prep_value = self.to_python(value)
        if prep_value.self_closed:
            return self.to_python(value).meta_content
        else:
            return self.to_python(value).tag_value

    def db_type(self, connection):
        return 'VARCHAR(%s)' % self.max_length


class TitleTagField(with_metaclass(models.SubfieldBase, BaseTagField)):
    """
    Creates a field for Title Tag
    * Not Null
    * Not Blank
    * Max-length 68
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
        title_tag = TitleTag(**{'value': title})
        return title_tag


class MetaTagField(with_metaclass(models.SubfieldBase, BaseTagField)):
    """
    Creates a field for Meta Tag
    * Max-length 255
    """
    description = "Field for Storing <meta /> tag"

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['db_index'] = False
        kwargs['null'] = True
        kwargs['max_length'] = 255
        super(MetaTagField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, MetaTag):
            return value
        content = super(MetaTagField, self).to_python(value)
        meta_tag = MetaTag(**{'name': self.name, 'value': content})
        return meta_tag


class KeywordsTagField(with_metaclass(models.SubfieldBase, BaseTagField)):
    """
    Creates a field for Keywords Meta Tag
    * Max-length 255
    """
    description = "Field for Storing <meta name='keywords' /> tag"

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['db_index'] = False
        kwargs['null'] = True
        kwargs['max_length'] = 255
        self.name = 'keywords'
        super(KeywordsTagField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, KeywordsTag):
            return value
        keywords = super(KeywordsTagField, self).to_python(value)
        keyword_tag = KeywordsTag(**{'name': self.name, 'value': keywords})
        return keyword_tag