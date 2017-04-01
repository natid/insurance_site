import config

__author__ = 'magenn'

from threading import Thread
from time import sleep
from insurance_crm.dal import dal_django
from insurance_crm.mail import gmail_manager

class MailScanner():
    def __init__(self, hours_interval = 24):
        self.hours_interval = hours_interval
        self._daily_mails_parser()
        #thread = Thread(target = self.start_timed_crawler_thread)
        #thread.start()

    def start_timed_crawler_thread(self):
        while(True):
            self._daily_mails_parser()
            sleep(self.hours_interval*3600)

    def _daily_mails_parser(self):
        threads = gmail_manager.get_threads_by_query(query=config.GMAIL_QUERY)
        for thread in threads:
            mails = gmail_manager.get_mails_for_thread(thread)
            mails_with_attachments = gmail_manager.get_attachments_for_message(mails)
            mail_details = gmail_manager.get_mail_details(mails)
            if mail_details:
                dal_django.add_mails_to_client(mails_with_attachments, mail_details["customer_id"], mail_details["company_email"].split("@")[1])
                gmail_manager.set_thread_as_read(thread)