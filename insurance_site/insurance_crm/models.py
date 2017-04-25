from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

@python_2_unicode_compatible
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return "Agent: {} {}".format(self.first_name, self.last_name)

@python_2_unicode_compatible
class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    agent = models.ForeignKey(Agent)
    status = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    id_number = models.CharField(max_length=20)

    def __str__(self):
        return "Client: {}".format(self.first_name, self.last_name)

@python_2_unicode_compatible
class InsuranceCompany(models.Model):
    name = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    additional_domains = models.CharField(max_length=500)
    clients = models.ManyToManyField(Client, through='ResponseMail')

    def __str__(self):
        return "Insurance company: {}".format(self.name)

@python_2_unicode_compatible
class ResponseMail(models.Model):
    client = models.ForeignKey(Client)
    insurance_company = models.ForeignKey(InsuranceCompany)
    mail = models.TextField(max_length=50)
    date_received = models.DateField()

    def __str__(self):
        return "ResponseMails: {}".format(self.id)

@python_2_unicode_compatible
class Attachment(models.Model):
    response_mail = models.ForeignKey(ResponseMail)
    attachment = models.TextField(max_length=50000)
    filename = models.CharField(max_length=100)

    def __str__(self):
        return "Attachment: {}".format(self.id)

@python_2_unicode_compatible
class SignedPdf(models.Model):
    client = models.ForeignKey(Client)
    pdf_file = models.TextField(max_length=50000)

    def __str__(self):
        return "Signed Pdf: {}".format(self.id)

@python_2_unicode_compatible
class Credentials(models.Model):
    credentials_file = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return "credentials file"
