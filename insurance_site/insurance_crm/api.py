from rest_framework.generics import ListAPIView

from .serializers import ClientSerializer, AgentSerializer
from .models import Client, Agent

class ClientApi(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class AgentApi(ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer