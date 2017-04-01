# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from server.cellosign import send_sign_document_request_to_client
from django.http import HttpResponse
from insurance_crm.server.mail_scanner import MailScanner
from django.shortcuts import render_to_response, render, redirect
import base64
import os
from insurance_crm.dal import dal_django
import server.config
from insurance_crm.mail import gmail_manager
from insurance_crm.server import config

def send_cellosign_request(request):
    client_id = request.GET.get("id")
    res = send_sign_document_request_to_client(client_id)
    return HttpResponse("OK")

def run_mail_scanner(request):
    MailScanner()

    #temporary to make sure that the API is called once a day
    message = gmail_manager.create_message(config.MAIL_ADDRESS, "magenheim@gmail.com", "runned mail scanner", "")
    gmail_manager.send_mail(config.MAIL_ADDRESS, message)

    return HttpResponse("OK")

@csrf_exempt
#this function is after we got the confirmed signed document and it's path is in the DB
def get_pdf_from_cellosign(request):
    client = dal_django.get_client_from_id(request.POST.get("client_id"))
    pdf_encoded = request.POST.get("PdfFile")
    pdf_file = base64.urlsafe_b64decode(str(pdf_encoded))
    dal_django.add_cellosign_pdf_response(client, pdf_file)
    message_title = config.MESSAGE_TITLE_TEMPLATE.format(client.name, client.id)
    message_body = config.MESSAGE_BODY_TEMPLATE.format(client.agent.first_name + client.agent.last_name, client.agent.license_number, client.agent.phone_number)
    sender_email = config.MAIL_ADDRESS.replace("@", "+{0}@".format(str(client.id)))
    for company in dal_django.get_insurance_companies():
        message = gmail_manager.create_message_with_attachment(
            sender_email, company.mail, message_title, message_body, pdf_file)
        gmail_manager.send_mail(sender_email, message)
    return HttpResponse("OK")

def return_main_page(request):
    return redirect("https://d3p5dvqck1wwt9.cloudfront.net/dist/index.html")
