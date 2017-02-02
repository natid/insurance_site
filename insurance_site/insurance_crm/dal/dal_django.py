__author__ = 'magenn'

from insurance_crm.models import Client, Agent, InsuranceCompany, ResponseMails


def get_client_from_name(client_name):
    return Agent.objects.get(name=client_name)

def get_client_from_id(client_id):
    return Agent.objects.get(id=client_id)

def add_agent(name, id, number, email, license_number):
    return Agent.objects.create(name=name, id=id, phone_number=number, email=email, license_number=license_number)

def get_agent(agent_name):
    return Agent.objects.get(name=agent_name)

def get_insurance_companies():
    return InsuranceCompany.objects.get()

def update_client_pdf_location(client, signed_file_path):
    client.signed_file_path = signed_file_path
    client.save()

def add_mails_to_client(self, attachments, customer_id, insurance_company, mails):
    attachments_for_db = [attachment.encode("base64") for attachment in attachments]
    ResponseMails.objects.create(customer_id = customer_id, insurance_company = insurance_company, mails = mails, attachments = attachments_for_db)