# -*- coding: utf-8 -*-
from celery.task import task
from utils.email_util import send_reply_mail, send_error_email

@task
def send_email_task(receiver, title, content, did, username, diary_title):
    send_reply_mail(receiver, title, content, did, username, diary_title)


@task
def send_error_email_task(title, error_log):
    send_error_email(title, error_log)
