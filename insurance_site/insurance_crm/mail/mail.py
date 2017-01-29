from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import base64
from apiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_threads_by_query(query=''):
    response = _get_service().users().threads().list(userId="me", q=query).execute()
    threads = []
    if 'threads' in response:
        threads.extend(response['threads'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = _get_service().users().threads().list(userId="me", q=query,geToken=page_token).execute()
        threads.extend(response['threads'])

    return threads

def _get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('gmail', 'v1', http=http)


def get_mails_for_thread(thread):
    return _get_service().users().threads().get(userId="me", id=thread["id"]).execute()["messages"]


def GetAttachments(service, user_id, msg_id, store_dir):
  """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    store_dir: The directory used to store attachments.
  """
  try:
      message = service.users().messages().get(userId=user_id, id=msg_id).execute()


      for part in message['payload']['parts']:
          if part['filename']:
            if 'data' in part['body']:
                data = part['body']['data']
            else:
                attachment = service.users().messages().attachments().get(
                    userId=user_id, messageId=msg_id,id=part["body"]["attachmentId"]).execute()

                data = attachment['data']


            data = data.encode('UTF-8')
            #data = data.replace('-', '+')
            #data = data.replace('_', '/')

            file_data = base64.urlsafe_b64decode(data)
            #file_data = base64.b64decode(data)
            #file_data = file_data[:-1]

            path = '\\'.join([store_dir, part['filename']])

            f = open(path, 'wb')
            f.write(file_data)
            f.close()


  except errors.HttpError, error:
    print('An error occurred: %s' % error)


def main():

    service = _get_service()
    threads = get_threads_by_query()
    mails = get_mails_for_thread(threads[0])

    GetAttachments(service, "me", mails[0]["id"], r"D:\temp")



    """
    threads = get_threads_by_query()
    mails = get_mails_for_thread(threads[0])

    for mail in mails:
        attachment = _get_service().users().messages().attachments().get(
            userId="me", messageId=mail["id"], id=mail["payload"]["parts"][1]["body"]["attachmentId"]).execute()


        print (attachment)

    """


if __name__ == '__main__':
    main()