from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .serializers import ClientSerializer, AgentSerializer
from .models import Client, Agent
from rest_framework.request import Request
from rest_framework.response import Response
from permissions import IsTheAgent
from rest_framework.decorators import detail_route, list_route


class ClientViewSet(ModelViewSet):
    #queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsTheAgent,)

    """
    @list_route()
    def agent_clients(self, request):
        agent_clients = Client.objects.filter(agent__user=request.user)

        serializer = self.get_serializer(agent_clients, many=True)
        return Response(serializer.data)
    """

    def get_queryset(self):
        return Client.objects.filter(agent__user=self.request.user)


class AgentViewSet(ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ClientList(ListAPIView):

    def get_queryset(self):
        user = self.request.user


