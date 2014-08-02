from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.six import iteritems


@python_2_unicode_compatible
class BaseTag(object):
    """
    Base Tag behaviour
    """
    tag_name = ""
    self_closed = True  # Defines if should close itself < />
    attributes = {}
    tag_value = ""

    def print_tag(self):

        """
        Builds tag as text for printing
        :return: text
        """
        if not isinstance(self, BaseTag):
            raise TypeError("Tag must be of class simple-seo.tags.BaseTag")

        print_attrs = ""
        for attr_name, attr_value in iteritems(self.attributes):
            print_attrs += " %s=\"%s\"" % (attr_name, attr_value)

        if self.self_closed:
            return "<%s %s />" % (self.tag_name, print_attrs)
        else:
            return "<%s %s>%s</%s>" % (self.tag_name, print_attrs, self.tag_value, self.tag_name)

    def __str__(self):
        return self.print_tag()

    def __len__(self):
        return len(self.tag_value)


class TitleTag(BaseTag):
    """
    Title Tag class
    """
    def __init__(self, *args, **kwargs):
        self.tag_name = "title"
        self.self_closed = False
        if 'value' in kwargs:
            if len(kwargs['value']) > 68:
                self.tag_value = kwargs['value'][:68]
            else:
                self.tag_value = kwargs['value']
        super(TitleTag, self).__init__()
