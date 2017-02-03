from .api import ClientViewSet, AgentViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
import views


router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'agents', AgentViewSet)

urlpatterns = router.urls

urlpatterns.append(url(r'^nir/', views.nir))