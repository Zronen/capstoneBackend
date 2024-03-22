from django.contrib import admin
from .models import Keyword, WebResource, Message

admin.site.register(Keyword)
admin.site.register(WebResource)
admin.site.register(Message)