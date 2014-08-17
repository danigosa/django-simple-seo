from __future__ import unicode_literals
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import FieldFile
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.staticfiles.storage import staticfiles_storage


@python_2_unicode_compatible
class BaseTag(object):
    """
    Base Tag behaviour
    """
    tag_name = ""
    self_closed = True  # Defines if should close itself < />
    meta_name = ""
    meta_content = ""
    tag_value = ""

    def __init__(
            self,
            tag_name=None,
            self_closed=None,
            meta_name=None,
            meta_content=None,
            tag_value=None):
        """
        Explicit Initialization of Tag
        :param tag_name:
        :param self_closed:
        :param meta_name:
        :param meta_content:
        :param tag_value:
        :return:
        """
        if tag_name:
            self.tag_name = tag_name
        if tag_value:
            self.tag_value = tag_value
        if self_closed is not None:
            self.self_closed = self_closed
        if meta_name:
            self.meta_name = meta_name
        if meta_content:
            self.meta_content = meta_content

    def print_tag(self):
        """
        Builds tag as text for printing
        :return: text
        """
        if not isinstance(self, BaseTag) and not issubclass(self, BaseTag):
            raise TypeError("Tag must be of class simple-seo.tags.BaseTag")

        if self.self_closed:
            if self.meta_name and self.meta_content:
                return "<%s name=\"%s\" content=\"%s\" />" % (self.tag_name, self.meta_name, self.meta_content)
            else:
                return ""
        else:
            if self.tag_value:
                return "<%s>%s</%s>" % (self.tag_name, self.tag_value, self.tag_name)
            else:
                return ""

    def __str__(self):
        if self.self_closed:
            if self.meta_content is None:
                return ''
            return self.meta_content
        else:
            if self.tag_value is None:
                return ''
            return self.tag_value

    def __len__(self):
        raise NotImplementedError("Must implement tag output __len__()")


class TitleTag(BaseTag):
    """
    Title Tag class
    """

    def __init__(self, tag_name=None, self_closed=None, meta_name=None, meta_content=None, tag_value=None, *args,
                 **kwargs):
        super(TitleTag, self).__init__(tag_name=tag_name, self_closed=self_closed, meta_name=meta_name,
                                       meta_content=meta_content, tag_value=tag_value)
        self.tag_name = "title"
        self.self_closed = False
        if 'value' in kwargs:

            if kwargs['value'] and len(kwargs['value']) > 68:
                self.tag_value = kwargs['value'][:68]
            else:
                self.tag_value = kwargs['value']

    def __str__(self):
        if self.tag_value is None:
            return ''
        return self.tag_value

    def __len__(self):
        if self.tag_value is None:
            return 0
        return len(self.tag_value)


class BaseMetatag(BaseTag):
    """
    Base Meta Tag
    """

    def __init__(self, tag_name=None, self_closed=None, meta_name=None, meta_content=None, tag_value=None, *args,
                 **kwargs):
        super(BaseMetatag, self).__init__(tag_name=tag_name, self_closed=self_closed, meta_name=meta_name,
                                          meta_content=meta_content, tag_value=tag_value)

        self.tag_name = 'meta'
        self.self_closed = True
        if 'name' in kwargs:
            self.meta_name = kwargs['name']

    def __str__(self):
        if self.meta_content is None:
            return ''
        return self.meta_content

    def __len__(self):
        if self.meta_content is None:
            return 0
        return len(self.meta_content)


class MetaTag(BaseMetatag):
    """
    Meta Tag class
    """

    def __init__(self, tag_name=None, self_closed=None, meta_name=None, meta_content=None, tag_value=None, *args,
                 **kwargs):
        super(BaseMetatag, self).__init__(tag_name=tag_name, self_closed=self_closed, meta_name=meta_name,
                                          meta_content=meta_content, tag_value=tag_value)
        self.tag_name = 'meta'
        if 'value' in kwargs:
            if kwargs['value'] and len(kwargs['value']) > 255:
                self.meta_content = kwargs['value'][:255]
            else:
                self.meta_content = kwargs['value']


class ImageMetaTag(BaseMetatag):
    """
    Image Meta Tag class
    """

    def __init__(self, tag_name=None, self_closed=None, meta_name=None, meta_content=None, tag_value=None, *args,
                 **kwargs):
        super(ImageMetaTag, self).__init__(tag_name=tag_name, self_closed=self_closed, meta_name=meta_name,
                                           meta_content=meta_content, tag_value=tag_value)
        self.tag_name = 'meta'
        if 'value' in kwargs:
            if kwargs['value']:
                if isinstance(kwargs['value'], InMemoryUploadedFile):
                    self._inmemoryuploadedfile = kwargs['value']
                    self.meta_content = kwargs['path'] + kwargs['value']._name
                else:
                    self._inmemoryuploadedfile = None
                    # It's not an upload, just reading
                    if isinstance(kwargs['value'], FieldFile):
                        self.meta_content = kwargs['value'].name
                    elif isinstance(kwargs['value'], ImageMetaTag):
                        self.meta_content = kwargs['value'].meta_content
                    else:
                        self.meta_content = kwargs['value']

    @property
    def url(self):
        return staticfiles_storage.url(self.meta_content)

    def __str__(self):
        if self.meta_content is None:
            return ''
        return self.meta_content


class KeywordsTag(BaseMetatag):
    """
    Keywords Meta Tag class
    """

    @staticmethod
    def _clean(value):
        if value:
            return value.replace('"', '&#34;').replace("\n", ", ").strip()
        else:
            return value

    def __init__(self, tag_name=None, self_closed=None, meta_name=None, meta_content=None, tag_value=None, *args,
                 **kwargs):
        super(KeywordsTag, self).__init__(tag_name=tag_name, self_closed=self_closed, meta_name=meta_name,
                                          meta_content=meta_content, tag_value=tag_value)
        self.tag_name = 'meta'
        if 'value' in kwargs:
            if kwargs['value'] and len(kwargs['value']) > 255:
                self.meta_content = self._clean(kwargs['value'][:255])
            else:
                self.meta_content = self._clean(kwargs['value'])
