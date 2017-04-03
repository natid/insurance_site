from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .serializers import ClientSerializer, AgentSerializer, ResponseMailSerializer
from .models import Client, Agent, ResponseMail, InsuranceCompany, Attachment
from rest_framework.request import Request
from rest_framework.response import Response
from permissions import IsTheAgent
from rest_framework.decorators import detail_route, list_route
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
import base64


class ResponseMailViewSet(ViewSet):

    def list(self, request):
        queryset = ResponseMail.objects.all()
        serializer = ResponseMailSerializer(queryset, many=True)
        return Response(serializer.data)



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
        #return Client.objects.filter(agent__user=self.request.user)
        return Client.objects.all()


class AgentViewSet(ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ResponseMailViewSet(ModelViewSet):
    queryset = ResponseMail.objects.all()
    serializer_class = ResponseMailSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ClientList(ListAPIView):

    def get_queryset(self):
        user = self.request.user


@api_view(['GET'])
def insurance_company_list(request):
        all_insurance_companies = InsuranceCompany.objects.distinct()

        #client_mails = ResponseMail.objects.filter(client__agent__user=request.user)

        client_id = request.GET.get("client_id")
        client_mails = ResponseMail.objects.filter(client__id=client_id)
        companies_in_mails = set([x.insurance_company for x in client_mails])

        data = []

        for ic in all_insurance_companies:

            if ic in companies_in_mails:
                data.append({
                    "id": ic.id,
                    "name": ic.name,
                    "status": True
                })
            else:
                data.append({
                    "id": ic.id,
                    "name": ic.name,
                    "status": False
                })

        return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_response_mail_data(request):
    insurance_company_id = request.GET.get("insurance_company_id")
    client_id = request.GET.get("client_id")
    company_mails = ResponseMail.objects.filter(insurance_company__id=insurance_company_id, client__id=client_id)

    response = []

    for company_mail in company_mails:
        mail_resp = {}
        mail_data = json.loads(company_mail.mail)

        data = ""
        for part in mail_data["payload"]["parts"]:

            data += str(part["body"]["data"])

        mail_resp["text"] = base64.urlsafe_b64decode(data)

        attachments = Attachment.object.filter(response_mail=company_mail)

        mail_resp["attachments"] = []

        for attachment in attachments:
            mail_resp["attachments"].append(attachment.attachment)

        response.append(mail_resp)

    return JsonResponse(response, safe=False)