# -*- coding: utf-8 -*-
from __future__ import print_function
from insurance_crm.server import config
import base64
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os
from googleapiclient import discovery
#from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
from insurance_crm.dal import dal_django

_credentials_loaded_from_db = False

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

def get_service():
    global _credentials_loaded_from_db

    if (not _credentials_loaded_from_db):
        dal_django.load_credentials_from_db(_get_credentials_path(config.HOME_DIR))
        _credentials_loaded_from_db = True

    credentials = get_credentials(config.HOME_DIR)
    http = credentials.authorize(httplib2.Http())
    return discovery.build('gmail', 'v1', http=http)

def _get_credentials_path(home_dir):
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    return os.path.join(credential_dir,'gmail-python-quickstart.json')

def get_credentials(home_dir):
    credential_path = _get_credentials_path(home_dir)
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(config.CLIENT_SECRET_FILE, config.SCOPES)
        flow.user_agent = config.APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        dal_django.store_credentials_to_db(credential_path)
    return credentials

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}


def create_message_with_attachment(sender, to, subject, message_text, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(file)
    filename = "signed_pdf.pdf"
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def get_threads_by_query(query=''):
    response = get_service().users().threads().list(userId="me", q=query).execute()
    threads = []
    if 'threads' in response:
        threads.extend(response['threads'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = get_service().users().threads().list(userId="me", q=query, pageToken=page_token).execute()
        threads.extend(response['threads'])

    return threads

def get_comapny_email(header):
    if "<" in header["value"]:
        return header["value"].split("<")[1][:-1]
    else:
        return header["value"]

#hasn't been tested yet
def try_get_customer_id_from_mails(mail, ids):
    customer_id = None
    raw_mail = unicode(get_raw_message_from_id(mail["id"]), errors='ignore')
    for id in ids:
        if id[1] in raw_mail or str(int(id[1])) in raw_mail:
            if customer_id != id[0] and customer_id is not None:
                return #raise Exception("an emial with 2 ids was found!!!!! need to do the hash redesign...")
            customer_id = id[0]
    return customer_id

def get_mail_details(mail):
    ids = dal_django.get_all_customer_ids()
    details = {}
    for header in mail["payload"]["headers"]:
        if header["name"] == "To" and "+" in header["value"]:
            customer_id = header["value"].split("+")[1].split("@")[0].replace("_", " ")
            if int(customer_id) in [x[0] for x in ids]:
                details["customer_id"] = customer_id
        if header["name"] == "From":
            details["company_email"] = get_comapny_email(header)

    if not details.has_key("customer_id"):
        customer_id = try_get_customer_id_from_mails(mail, ids)
        if customer_id:
            details["customer_id"] = customer_id

    if set(("customer_id", "company_email")) == set(details):
        return details


def set_thread_as_read(thread):
    return get_service().users().threads().modify(userId="me", id=thread['id'],body={'removeLabelIds': ["INBOX"]}).execute()

def set_thread_as_ignored(thread, ignored):
    if ignored:
        add_remove = 'addLabelIds'
    else:
        add_remove = 'removeLabelIds'
    return get_service().users().threads().modify(userId="me", id=thread['id'],body={add_remove: ["Label_2"]}).execute()

def set_thread_as_mapped(thread):
    return get_service().users().threads().modify(userId="me", id=thread['id'],body={'addLabelIds': ["Label_3"]}).execute()

def get_mails_for_thread(thread):
    return get_service().users().threads().get(userId="me", id=thread["id"]).execute()["messages"]

def send_mail(mail_from, message):
    return get_service().users().messages().send(userId="me", body=message).execute()

def get_raw_message_from_id(msg_id):
    return base64.urlsafe_b64decode(get_service().users().messages().get(userId="me", id=msg_id, format='raw').execute()["raw"].encode("ASCII"))


def get_attachments_for_message(mail):
    attachments = []
    attachments_for_mail = []
    if not mail["payload"].has_key("parts"):
        return
    for part in mail["payload"]["parts"]:
        if part["filename"]:
            if part["filename"].lower() == "signed_pdf.pdf":
                continue
            if part["body"].has_key("data"):
                attachment = part["body"]["data"]
            else:
                response = get_service().users().messages().attachments().get(
                    userId="me", messageId=mail["id"],id=part["body"]["attachmentId"]).execute()
                attachment = response["data"]
            decoded_attachment = base64.urlsafe_b64decode(attachment.encode("UTF-8"))
            attachments_for_mail.append((decoded_attachment, part["filename"]))
        raw_mail = get_raw_message_from_id(mail["id"])
        attachments.append((raw_mail,attachments_for_mail))
    return attachments


def insert_mail_to_db(thread):
    mails = get_mails_for_thread(thread)
    allocated = False
    for mail in mails:
        mail_details = get_mail_details(mail)
        mails_with_attachments = get_attachments_for_message(mail)
        if mail_details and mails_with_attachments:
            allocated = True
            dal_django.add_mails_to_client(mails_with_attachments, mail_details["customer_id"],
                                           mail_details["company_email"].split("@")[1], True)
    return allocated
