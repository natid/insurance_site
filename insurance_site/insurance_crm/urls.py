from .api import ClientViewSet, AgentViewSet
from rest_framework.routers import DefaultRouter
from views import send_cellosign_request, run_mail_scanner, get_pdf_from_cellosign
from django.conf.urls import url, include
import views


router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'agents', AgentViewSet)

urlpatterns = router.urls
urlpatterns.append(url(r'cellosign/', send_cellosign_request))
urlpatterns.append(url(r'return_cellosign_pdf', get_pdf_from_cellosign))
#TEMPORARY FOR TESTING
urlpatterns.append(url(r'run_mail_scanner/', run_mail_scanner))
