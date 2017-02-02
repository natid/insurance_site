from rest_framework.viewsets import ModelViewSet

from .serializers import ClientSerializer, AgentSerializer
from .models import Client, Agent


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class AgentViewSet(ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer