from .api import ClientViewSet, AgentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'agents', AgentViewSet)

urlpatterns = router.urls