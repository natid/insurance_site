# Create your views here.
from server.cellosign import send_sign_document_request_to_client
from django.http import HttpResponse
from insurance_crm.server.mail_scanner import MailScanner
from django.shortcuts import render_to_response

def send_cellosign_request(request):
    client_id = request.GET.get("id")
    res = send_sign_document_request_to_client(client_id)
    return HttpResponse("OK")

def run_mail_scanner(request):
    MailScanner()
    return HttpResponse("OK")
