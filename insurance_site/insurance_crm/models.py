from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

@python_2_unicode_compatible
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return "Agent: {}".format(self.name)

@python_2_unicode_compatible
class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True)
    notes = models.TextField(blank=True, null=True)
    agent = models.ForeignKey(Agent, related_name="clients")
    status = models.CharField(max_length=50, null=True)
    signed_file_path = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, null=True)

    def __str__(self):
        return "Client: {}".format(self.name)

@python_2_unicode_compatible
class InsuranceCompany(models.Model):
    name = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)

    def __str__(self):
        return "Insurance company: {}".format(self.name)

@python_2_unicode_compatible
class ResponseMail(models.Model):
    customer = models.ForeignKey(Client, related_name="identification_number")
    insurance_company = models.ForeignKey(InsuranceCompany, related_name="number")
    mail = models.TextField(max_length=50)

    def __str__(self):
        return "ResponseMails: {}".format(self.id)

@python_2_unicode_compatible
class Attachment(models.Model):
    response_mail = models.ForeignKey(ResponseMail, related_name="attachment_ids")
    attachment = models.TextField(max_length=50)

    def __str__(self):
        return "Attachment: {}".format(self.id)

