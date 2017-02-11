from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .serializers import ClientSerializer, AgentSerializer
from .models import Client, Agent
from rest_framework.request import Request


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticated,)


class AgentViewSet(ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = (permissions.IsAuthenticated,)