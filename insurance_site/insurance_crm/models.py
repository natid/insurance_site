from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

# Create your models here.

@python_2_unicode_compatible
class Agent(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return "Agent: {}".format(self.name)

@python_2_unicode_compatible
class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    agent = models.ForeignKey(Agent, related_name="clients")
    status = models.CharField(max_length=50)


    def __str__(self):
        return "Client: {}".format(self.name)





