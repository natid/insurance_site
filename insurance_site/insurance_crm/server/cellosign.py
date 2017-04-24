# -*- coding: utf-8 -*-
import config

__author__ = 'magenn'

import requests
import json
import base64
from insurance_crm.dal import dal_django
from insurance_site import settings

def send_sign_document_request_to_client(client_id):
    client = dal_django.get_client_from_id(client_id)
    agent = client.agent
    agent_name = agent.first_name + " " + agent.last_name

    headers = {'Content-type': 'application/json',
               'Accept': 'application/json',
               "Authorization": "Token  {0}".format(settings.CELLOSIGN_AUTHORIZATION_TOKEN)
               }

    inputvalues = {
        "client_name":"%s %s" % (client.first_name, client.last_name),
        "client_id":client.id_number,
        "agent_name":agent_name,
        "agent_name_2":agent_name,
        "agent_license_number":agent.license_number,
        "agent_phone":agent.phone_number,
    }
    data ={
        "input_file": inputvalues,
        "destination": client.phone_number,  # post SMS w/link to client
        "template": "bd343311cd4645078c9fd94b5b1960b3",
        "rep_email": config.MAIL_ADDRESS,
        "client_redirect": "http://www.google.com",
        "invite_message": config.CLIENT_INVITE_MESSAGE,
        "client_id": client.id
    }
    json_file = json.dumps(data)

    request = requests.post(config.CELLOSIGN_REQUEST_ADDRESS,
                            headers=headers, data=json_file)

    #return request
    return "NIR"


'''
data={
    "client_copy": "omer@cellosign.com",
    "rep_email": ["omer@cellosign.com","iris@cellosign.com"],
    "template":"283c6009a4aa4b1e89ca3ac6b880f25b" 
}
input_file = {
    "customer_name" : "קובי שגב",
    "customer_id": "028732436"
}
data['input_file'] = input_file
data = json.dumps(data)
 
request = requests.post('http://test.cellosign.com/ayalon/rep/create_session',headers=headers,data=data)

'''