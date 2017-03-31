__author__ = 'magenn'

from insurance_crm.models import Client, InsuranceCompany, ResponseMail, Attachment, SignedPdf, Credentials


def get_client_from_name(client_name):
    return Client.objects.get(name=str(client_name))

def get_client_from_id(client_id):
    return Client.objects.get(id=client_id)

def get_insurance_companies():
    return InsuranceCompany.objects.all()

def add_cellosign_pdf_response(customer, pdf_file):
    SignedPdf.objects.create(customer_id = customer.id, pdf_file = pdf_file)

def add_mails_to_client(mails_with_attachments, customer_name, insurance_company_email):
    customer = get_client_from_name(customer_name)
    insurance_company = InsuranceCompany.objects.get(mail=str(insurance_company_email))
    for mail in mails_with_attachments:
        attachments_for_db = [attachment.encode("base64") for attachment in mail[1]]
        response_mail = ResponseMail.objects.create(customer_id = customer.id, insurance_company = insurance_company, mail = mail[0])
        for attachment in attachments_for_db:
            Attachment.objects.create(response_mail_id = response_mail.id, attachment = attachment)

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

