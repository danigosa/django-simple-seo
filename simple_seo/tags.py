class BaseTag(object):
    """
    Base Tag behaviour
    """
    tag_name = ""
    self_closed = True  # Defines if should close itself < />
    attributes = {}


class TitleTag(BaseTag):
    """
    Title Tag class
    """
    def __init__(self, title=None, *args, **kwargs):
        self.tag_name = "title"
        self.self_closed = False
        if title and len(title) > 68:
            self.title = title[:68]
        super(TitleTag, self).__init__(*args, **kwargs)