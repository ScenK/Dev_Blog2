# -*- coding: utf-8 -*-
from utils.email_util import EmailUtil
from config import SmtpConfig

def send_email_task(receiver, title, content, did, username, diary_title):
    EmailUtil(SmtpConfig).send_reply_mail(receiver, title, content, did, username, diary_title)

def send_error_email_task(title, error_log):
    EmailUtil(SmtpConfig).send_error_email(title, error_log)
