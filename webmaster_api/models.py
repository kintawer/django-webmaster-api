from django.db import models
from datetime import datetime

# Create your models here.


class Table(models.Model):

    domain = models.CharField(blank=True, max_length=100)
    fatal = models.IntegerField(null=True, default=0)
    critical = models.IntegerField(null=True, default=0)
    possible_problem = models.IntegerField(null=True, default=0)
    recommendation = models.IntegerField(null=True, default=0)
    sitemap_date = models.DateField(null=True, blank=True)
    sitemap_url_count = models.IntegerField(null=True, default=0)
    searchable_date = models.DateField(null=True, blank=True)
    searchable_count = models.IntegerField(null=True, default=0)
