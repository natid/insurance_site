import base64
import os
from insurance_crm.dal import dal_django
import cellosign
import config
from insurance_crm.mail import gmail_manager


#this function is after we got the confirmed signed document and it's path is in the DB
def get_pdf_from_cellosign(response):
    client = dal_django.get_client_from_id(response["client_id"])
    pdf_file = base64.urlsafe_b64decode(response["PdfFile"])
    file_path = "".join((os.getcwd(), "\\", client.name, ".pdf"))
    with open(file_path, "b+") as file:
        file.write(pdf_file)
    dal_django.update_client_pdf_location(client, file_path)
    message_title = config.MESSAGE_TITLE_TEMPLATE.format(client.name, client.id)
    message_body = config.MESSAGE_BODY_TEMPLATE.format(client.agent.name, client.agent.license_number, client.agent.phone_number)
    sender_email = config.MAIL_ADDRESS.replace("@", "+{0}@".format(str(client.id)))
    for company in dal_django.get_insurance_companies:
        message = gmail_manager.create_message_with_attachment(
            sender_email, company.mail, message_title, message_body, client.signed_file_path)
        gmail_manager.send_mail(sender_email, message)