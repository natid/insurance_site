from django.conf.urls import url
from django.views.generic import TemplateView

from .api import ClientApi, AgentApi

urlpatterns = [
    url(r'^clients$', ClientApi.as_view()),
    url(r'^Agents$', AgentApi.as_view()),
    url(r'^home', TemplateView.as_view(template_name="insurance_crm/home.html")),
]