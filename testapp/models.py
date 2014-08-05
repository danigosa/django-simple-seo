from simple_seo.models import BaseMetadata
from simple_seo import register


class MyMetadata(BaseMetadata):
    """
    My Seo Model
    """

# Register SEO Model
register(MyMetadata)