# -*- coding: utf-8 -*-
__author__ = 'magenn'

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
MAIL_ADDRESS = "mgmt.insure@gmail.com"
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

#the only path available in AWS lambda
HOME_DIR = "/tmp"

GMAIL_QUERY = "label=Inbox is:unread"

MESSAGE_TITLE_TEMPLATE = u" בקשה לקבלת מידע לפי חוזר הצירוף ללקוח {0} ת.ז. {1}"
MESSAGE_BODY_TEMPLATE = """
אנא שלחו הפרטים במייל חוזר
פרטי בעל הרשיון:
{0}
מספר רשיון {1}
טל' נייד: {2}
"""

CLIENT_INVITE_MESSAGE = "שלום כיתה א"
CELLOSIGN_REQUEST_ADDRESS = 'http://test.cellosign.com/777/rep/create_session'