__author__ = 'magenn'

from insurance_crm.models import Client, InsuranceCompany, ResponseMail, Attachment, SignedPdf, Credentials
import json

def get_client_from_id(client_id):
    return Client.objects.get(id=client_id)

def get_insurance_companies():
    return InsuranceCompany.objects.all()

def add_cellosign_pdf_response(customer, pdf_file):
    SignedPdf.objects.create(client_id = customer.id, pdf_file = pdf_file)

def add_mails_to_client(mails_with_attachments, customer_id, insurance_company_domain, ignore_errors = True):
    try:
        insurance_company = [x for x in get_insurance_companies()
                             if x.mail.split("@")[1] == insurance_company_domain
                             or (x.additional_domains and insurance_company_domain in x.additional_domains.split(","))][0]
    except Exception:
        pass
    for mail in mails_with_attachments:
        if ignore_errors:
            mail_json = json.dumps(unicode(mail[0], errors='ignore'))
        else:
            mail_json = json.dumps(unicode(mail[0]))

        response_mail = ResponseMail.objects.create(client_id = customer_id, insurance_company = insurance_company, mail = mail_json)
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

def get_all_customer_ids():
    ids = []
    for client in Client.objects.all():
        ids.append((client.id, client.id_number))
    return ids