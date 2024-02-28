from django.db import models

class Keyword(models.Model):
    name = models.CharField(max_length=255)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class WebResource(models.Model):
    siteName = models.CharField(max_length=255)
    siteID = models.IntegerField(default=0)
    siteURL = models.CharField(max_length=1000)
    siteKeywords = models.ManyToManyField(Keyword)

    def __str__(self):
        return self.siteName