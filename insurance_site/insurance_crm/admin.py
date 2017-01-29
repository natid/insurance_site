from django.contrib import admin
from .models import Client, Agent

# Register your models here.

admin.site.register(Client)
admin.site.register(Agent)