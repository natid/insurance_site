from django.contrib import admin
from .models import Client, Agent, InsuranceCompany, ResponseMail, Attachment

# Register your models here.

admin.site.register(Client)
admin.site.register(Agent)
admin.site.register(InsuranceCompany)
admin.site.register(ResponseMail)
admin.site.register(Attachment)