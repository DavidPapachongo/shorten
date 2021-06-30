from django.db import models
from datetime import datetime
from baseconv import  base62
from django.urls import reverse
from user_agents import parse



# Create your models here.

class UrlModel(models.Model):
    link = models.URLField(max_length = 200, blank=False)
    
    def id_as_base62(self):
        return base62.encode(self.id)
    
    
    def shorten_link(self):
        return reverse("link-redirect", args=[self.id_as_base62()])

class ClickModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    url = models.ForeignKey(UrlModel, on_delete=models.CASCADE)
    user_agent = models.TextField(blank=True, null=True)

    def browser(self):
        ua_string = self.user_agent
        if ua_string:
            user_agent = parse(ua_string)
            return user_agent.browser.family  
        else:
            return
            
