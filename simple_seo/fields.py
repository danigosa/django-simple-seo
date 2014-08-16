from django.db import models
from django.db.models.fields.files import FileField, FieldFile
from django.utils.six import with_metaclass
from django.conf import settings

from simple_seo.tags import (
    ImageMetaTag,
    TitleTag,
    MetaTag,
    KeywordsTag
)


def _clean_i18_name(field_name):
    """
    Cleans i18 suffix in case it exists
    """
    if field_name and len(field_name) > 3:
        suffix = field_name[-3:]
        if suffix.startswith('_'):
            lang = suffix[-2:]
            for l in getattr(settings, 'LANGUAGES', []):
                if l[0] == lang:
                    # It's a language suffix. Remove it
                    return field_name[:-3]
    return field_name


class BaseTagField(with_metaclass(models.SubfieldBase, models.CharField)):
    """
    Base Meta Tag behaviour
    """
    description = "A hand of cards (bridge style)"

    def get_prep_value(self, value):
        prep_value = self.to_python(value)
        if prep_value.self_closed:
            return prep_value.meta_content
        else:
            return prep_value.tag_value

    def db_type(self, connection):
        return 'VARCHAR(%s)' % self.max_length


class BaseURLTagField(with_metaclass(models.SubfieldBase, models.URLField)):
    """
    Base URL Meta Tag behaviour
    """
    description = "A hand of cards (bridge style)"

    def get_prep_value(self, value):
        prep_value = self.to_python(value)
        if prep_value.self_closed:
            return prep_value.meta_content
        else:
            return prep_value.tag_value


class BaseImageTagField(with_metaclass(models.SubfieldBase, models.ImageField)):
    """
    Base Image Meta Tag behaviour
    """
    description = "A hand of cards (bridge style)"

    def get_prep_value(self, value):
        prep_value = self.to_python(value)
        if prep_value.self_closed:
            return prep_value.meta_content
        else:
            return prep_value.tag_value

    def pre_save(self, model_instance, add):
        "Returns field's value just before saving."
        file = FieldFile(model_instance, self, super(FileField, self).pre_save(model_instance, add).meta_content)
        tag = super(FileField, self).pre_save(model_instance, add)  # Let's hack this
        if hasattr(tag, '_inmemoryuploadedfile') and getattr(tag, '_inmemoryuploadedfile'):
            file.save(file.name, tag._inmemoryuploadedfile, save=False)
        return file


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
        meta_tag = MetaTag(
            meta_name=_clean_i18_name(self.name),
            **{
                'name': _clean_i18_name(self.name),
                'value': content
            }
        )
        return meta_tag


class URLMetaTagField(with_metaclass(models.SubfieldBase, BaseURLTagField)):
    """
    Creates a field for URL Meta Tag
    """
    description = "Field for Storing <meta /> tag"

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['db_index'] = False
        kwargs['null'] = True
        super(URLMetaTagField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, MetaTag):
            return value
        content = super(URLMetaTagField, self).to_python(value)
        meta_tag = MetaTag(
            meta_name=_clean_i18_name(self.name),
            **{
                'name': _clean_i18_name(self.name),
                'value': content
            }
        )
        return meta_tag


class ImageMetaTagField(with_metaclass(models.SubfieldBase, BaseImageTagField)):
    """
    Creates a field for Image Meta Tag
    """
    description = "Field for Storing <meta /> tag"

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['db_index'] = False
        kwargs['null'] = True
        super(ImageMetaTagField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, ImageMetaTag):
            return value
        content = super(ImageMetaTagField, self).to_python(value)
        image_meta_tag = ImageMetaTag(
            meta_name=_clean_i18_name(self.name),
            **{
                'name': _clean_i18_name(self.name),
                'value': content,
                'path': self.upload_to
            }
        )
        return image_meta_tag


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
        keyword_tag = KeywordsTag(
            meta_name=_clean_i18_name(self.name),
            **{
                'name': _clean_i18_name(self.name),
                'value': keywords
            }
        )
        return keyword_tag