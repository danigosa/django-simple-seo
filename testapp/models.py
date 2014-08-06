from simple_seo.models import OpenGraphMetadata
from simple_seo import register


class MyMetadata(OpenGraphMetadata):
    """
    My Seo Model
    """

# Register SEO Model
register(MyMetadata)