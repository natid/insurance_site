from .api import ClientViewSet, AgentViewSet, ResponseMailViewSet
from rest_framework.routers import DefaultRouter
from views import send_cellosign_request, run_mail_scanner, get_pdf_from_cellosign, return_main_page
from django.conf.urls import url, include
from django.views.generic import TemplateView


router = DefaultRouter()
router.register(r'clients', ClientViewSet, base_name="client")
router.register(r'agents', AgentViewSet)
router.register(r'response_mail', ResponseMailViewSet)

urlpatterns = router.urls
urlpatterns.append(url(r'cellosign/', send_cellosign_request))
urlpatterns.append(url(r'return_cellosign_pdf', get_pdf_from_cellosign))
#TEMPORARY FOR TESTING
urlpatterns.append(url(r'run_mail_scanner/', run_mail_scanner))
#urlpatterns.append(url(r'^client_list', TemplateView.as_view(template_name="insurance_crm/client_list.html")))
urlpatterns.append(url(r'^fuse/', return_main_page))
