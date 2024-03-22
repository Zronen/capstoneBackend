from django.db import models
import json

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

class Message(models.Model):
    sender = models.CharField(max_length=255)
    description = models.CharField(max_length=100000)
    #myDescription = models.TextField(null=True)

    #def set_myDescription (self, lst):
     #   self.set_myDescription = json.dumps(lst)

    #def set_myDescription (self):
     #   return json.loads(self.set_myDescription)

    def __str__(self):
        return self.description