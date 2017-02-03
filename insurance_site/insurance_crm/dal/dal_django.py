__author__ = 'magenn'

from insurance_crm.models import Client, InsuranceCompany, ResponseMail, Attachment


def get_client_from_name(client_name):
    return Client.objects.get(name=str(client_name))

def get_client_from_id(client_id):
    return Client.objects.get(id=client_id)

def get_insurance_companies():
    return InsuranceCompany.objects.get()

def update_client_pdf_location(client, signed_file_path):
    client.signed_file_path = signed_file_path
    client.save()

def add_mails_to_client(mails_with_attachments, customer_name, insurance_company_email):
    customer = get_client_from_name(customer_name)
    insurance_company = InsuranceCompany.objects.get(mail=str(insurance_company_email))
    for mail in mails_with_attachments:
        attachments_for_db = [attachment.encode("base64") for attachment in mail[1]]
        response_mail = ResponseMail.objects.create(customer_id = customer.id, insurance_company = insurance_company, mail = mail[0])
        for attachment in attachments_for_db:
            Attachment.objects.create(response_mail_id = response_mail.id, attachment = attachment)