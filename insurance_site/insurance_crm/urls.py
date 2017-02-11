from .api import ClientViewSet, AgentViewSet
from rest_framework.routers import DefaultRouter
from views import send_cellosign_request, run_mail_scanner
from django.conf.urls import url, include
from django.views.generic import TemplateView


router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'agents', AgentViewSet)

urlpatterns = router.urls
urlpatterns.append(url(r'cellosign/', send_cellosign_request))

#TEMPORARY FOR TESTING
urlpatterns.append(url(r'run_mail_scanner/', run_mail_scanner))
#urlpatterns.append(url(r'^client_list', TemplateView.as_view(template_name="insurance_crm/client_list.html")))
