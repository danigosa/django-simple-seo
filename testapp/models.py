from simple_seo.models import BaseMetadata
from django.db import models


class MyMetadata(models.Model, BaseMetadata):
    """
    My Seo Model
    """
    test_field = models.CharField(max_length=25)
