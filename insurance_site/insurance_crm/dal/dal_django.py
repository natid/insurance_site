__author__ = 'magenn'

from insurance_crm.models import Client, InsuranceCompany, ResponseMail, Attachment, SignedPdf, Credentials
import json

def get_client_from_id(client_id):
    return Client.objects.get(id=client_id)

def get_insurance_companies():
    return InsuranceCompany.objects.all()

def add_cellosign_pdf_response(customer, pdf_file):
    SignedPdf.objects.create(client_id = customer.id, pdf_file = pdf_file)

def add_mails_to_client(mails_with_attachments, customer_id, insurance_company_domain):
    insurance_company = [x for x in get_insurance_companies() if x.mail.split("@")[1] == insurance_company_domain][0]
    for mail in mails_with_attachments:
        #attachments_for_db = [attachment.encode("base64") for attachment in mail[1]]
        response_mail = ResponseMail.objects.create(client_id = customer_id, insurance_company = insurance_company, mail = json.dumps(mail[0]))
        for attachment, filename in mail[1]:
            Attachment.objects.create(response_mail_id=response_mail.id, attachment=attachment.encode("base64"), filename=filename)

def _get_credential_entry():
    credentials = Credentials.objects.all()
    if not credentials.exists():
        return Credentials.objects.create()
    else:
        return credentials[0]

def load_credentials_from_db(credential_path):
    credential = _get_credential_entry()
    if credential:
        with open(credential_path, "w+") as f:
            f.write(str(credential.credentials_file))

def store_credentials_to_db(credential_path):
    credential = _get_credential_entry()
    with open(credential_path, "r") as f:
        credential.credentials_file = f.read()
        credential.save()

