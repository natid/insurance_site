from rest_framework import serializers

from .models import Client, Agent

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Client


class AgentSerializer(serializers.ModelSerializer):

    clients = ClientSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Agent