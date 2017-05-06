from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .serializers import ClientSerializer, AgentSerializer, ResponseMailSerializer
from .models import Client, Agent, ResponseMail, InsuranceCompany, Attachment
from rest_framework.response import Response
from permissions import IsTheAgent
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import json
import email
import quopri
from insurance_crm.mail import gmail_manager


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

    def create(self, request):
        agent_id = Agent.objects.filter(user=request.user)[0].id

        Client.objects.create(first_name=request.data.get('first_name',''),
                      last_name=request.data.get('last_name',''),
                      phone_number=request.data.get('phone_number',''),
                      agent_id=agent_id,
                      notes=request.data.get('notes',''),
                      status=request.data.get('status',''),
                      id_number=request.data.get('id_number',''),
                      )

        return HttpResponse(status=200)

    def get_queryset(self):
        return Client.objects.filter(agent__user=self.request.user)
        #return Client.objects.all()


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


def convert_raw_message_to_html(raw_msg):
    try:
        mail = email.message_from_string(raw_msg)
    except Exception:
        mail = email.message_from_string(raw_msg.encode("utf-8").decode("ascii", "ignore"))
    contents = []
    for part in mail.walk():
        if part.get_content_type() in ('text/plain', 'text/html'):
            charset = part.get_content_charset()
            if charset != None:
                if charset.upper() == "ISO-8859-8-I":
                    charset = "ISO-8859-8"
                payload_raw = part.get_payload()
                encoding = part.get('content-transfer-encoding', '').lower()
                if encoding == 'base64':
                    payload_raw = payload_raw.decode('base64')
                try:
                    payload = quopri.decodestring(payload_raw).decode(charset)
                except Exception:
                    try:
                        payload = quopri.decodestring(payload_raw).decode('utf-8')
                    except:
                        continue
            else:  # assume ascii
                try:
                    payload = quopri.decodestring(part.get_payload()).decode('ascii')
                except:
                    payload = part.get_payload()
            payload = payload.replace('\n', '<br>').replace("<br><br>","<br>")
            contents.append(payload)
        elif "image" in part.get_content_type():
            img_str = '<img src="data:{0};{1},{2}"/>'.format(part.get_content_type(), part.get('content-transfer-encoding', '').lower(), part.get_payload())
            contents.append(img_str)
    return contents

def replace_cid_images_with_html_tags(attachment, html_response):
    new_str = html_response
    index = new_str.lower().find("[cid:{0}".format(attachment.filename.lower()))
    if index != -1:
        img_str = '<img src="data:image/{0};base64,{1}"/>'.format(
            attachment.filename[attachment.filename.rfind(".")+1:],
            attachment.attachment)
        new_str = new_str[:index] + img_str + new_str[index + 1 + new_str[index:].find("]"):]

    index = new_str.lower().find('src="cid:{0}'.format(attachment.filename.lower()))
    if index != -1:
        img_str = 'src="data:image/{0};base64,{1}"'.format(
            attachment.filename[attachment.filename.rfind(".") + 1:],
            attachment.attachment)
        new_str = new_str[:index] + img_str + new_str[index + 1 + new_str[index:].find('"'):]

    return new_str

@api_view(['GET'])
def get_response_mail_data(request):
    insurance_company_id = request.GET.get("insurance_company_id")
    client_id = request.GET.get("client_id")
    company_mails = ResponseMail.objects.filter(insurance_company__id=insurance_company_id, client__id=client_id)

    response = []

    for company_mail in company_mails:
        mail_resp = {}
        mail_data = json.loads(company_mail.mail)

        '''
        data = ""
        for part in mail_data["payload"]["parts"]:

            if "data" in part["body"]:
                data += str(part["body"]["data"])

        if data == "":
            mail_resp["text"] = mail_data["snippet"]
        else:
            mail_resp["text"] = base64.urlsafe_b64decode(data)
        '''


        mail_resp["text"] = "".join(convert_raw_message_to_html(mail_data))

        attachments = Attachment.objects.filter(response_mail=company_mail)

        mail_resp["attachments"] = []

        for attachment in attachments:
            if attachment.filename.lower() == "signed_pdf.pdf":
                continue
            original_response = mail_resp["text"]
            while True:
                response_str = mail_resp["text"]
                mail_resp["text"] = replace_cid_images_with_html_tags(attachment, response_str)
                if response_str == mail_resp["text"]:
                    break
            if original_response == mail_resp["text"]:
                mail_resp["attachments"].append({"data": attachment.attachment, "filename": attachment.filename})

        response.append(mail_resp)

    return JsonResponse(response, safe=False)

#################################################################################33
#helper functions - didn't test them yet

def remove_duplicate_response_mails(request):
    responses = []
    to_delete = []
    for response in ResponseMail.objects.all():
        responses.append(response)

    for response1 in responses:
        for response2 in responses:
            if response1.id != response2.id and response1.mail == response2.mail:
                to_delete.append(response2)
                break

    to_delete = set(to_delete)
    for mail in to_delete:
        mail.delete()

    return HttpResponse("OK")

def rescan_mail_inbox(request):
    #remove all responses first
    for response in ResponseMail.objects.all():
        response.delete()

    #rescan all of the mails
    all_threads = gmail_manager.get_threads_by_query('!label:mapped')
    for thread in all_threads:
        gmail_manager.set_thread_as_ignored(thread, False)
        allocated = gmail_manager.insert_mail_to_db(thread)
        if not allocated:
            gmail_manager.set_thread_as_ignored(thread, True)
        else:
            gmail_manager.set_thread_as_mapped(thread)

    return HttpResponse("OK")
