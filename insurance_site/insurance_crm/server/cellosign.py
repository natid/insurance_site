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
    inputvalues = {
        "client_name":client.name,
        "client_id":client.id,
        "agent_name":agent_name,
        "agent_name_2":agent_name,
        "agent_license_number":agent.license_number,
        "agent_phone":agent.phone_number,
    }
    data ={
        "input_file": base64.b64encode(json.dumps(inputvalues))
    }
    json_file = json.dumps(data)

    headers = {'Content-type': 'application/json',
               'Accept': 'application/json',
               "Authorization": "Token  {0}".format(settings.CELLOSIGN_AUTHORIZATION_TOKEN)
    }
    params={
            "destination": client.phone_number, #post SMS w/link to client
            "template": "bd343311cd4645078c9fd94b5b1960b3",
            "rep_email":config.MAIL_ADDRESS,
            "client_redirect": "http://www.google.com",
            "invite_message": config.CLIENT_INVITE_MESSAGE,
            "client_id": client.id
    }
    request = requests.post(config.CELLOSIGN_REQUEST_ADDRESS,
                            headers=headers, params=params, data=json_file)

    #return request
    return "NIR"