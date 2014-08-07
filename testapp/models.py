from simple_seo.models import AllMetadata
from simple_seo import register


class MyMetadata(AllMetadata):
    """
    My Seo Model
    """

# Register SEO Model
register(MyMetadata)