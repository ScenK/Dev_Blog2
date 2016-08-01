# -*- coding: utf-8 -*-
import smtplib
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class EncodingFormatter(logging.Formatter):

    def __init__(self, fmt, datefmt=None, encoding=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.encoding = encoding

    def format(self, record):
        result = logging.Formatter.format(self, record)
        if isinstance(result, unicode):
            result = result.encode(self.encoding or 'utf-8')
            return result

class EmailUtil(object):
    def __init__(self, smtp_config):
        self.smtp_config = smtp_config

    def send_reply_mail(self, receiver, title, content, did, username, diary_title):
        sender = self.smtp_config.USER
        password = self.smtp_config.PASSWORD
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(title, "UTF-8")
        msg['From'] = sender
        msg['To'] = receiver
        content = self.generateHtml(content, did, username, diary_title)
        part = MIMEText(content, 'html', _charset='UTF-8')
        msg.attach(part)

        server = smtplib.SMTP(self.smtp_config.SERVER, self.smtp_config.PORT)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()


    def generateHtml(self, content, did, username, diary_title):
        avatar = ''
        html = u'<table style="width: 100%;"><thead style=" width: 100%;color: #FFF; height: 75px; background-color: #bdcadf; -webkit-box-shadow: 0 1px 1px rgba(255,255,255,.5), inset 0 1px 3px #183357; -moz-box-shadow: 0 1px 1px rgba(255,255,255,.5), inset 0 1px 3px #183357; box-shadow: 0 1px 1px rgba(255,255,255,.5), inset 0 1px 3px #183357; background-image: -webkit-linear-gradient(bottom, #647792, #8d9baf); background-image: -moz-linear-gradient(bottom, #647792, #8d9baf); background-image: -o-linear-gradient(bottom, #647792, #8d9baf); background-image: -ms-linear-gradient(bottom, #647792, #8d9baf); background-image: linear-gradient(to top, #647792, #8d9baf);"><tr><td colspan="2" style="padding: 5px 0 5px 2%;">'
        html += self.smtp_config.MAIN_TITLE
        html += u'</td></tr></thead><tbody><tr>'
        html += u'<td style="width: 25%;padding:10px 0;"><img src="' + \
            str(avatar) + '"></td><td><b>'
        html += username
        html += u'</b>:<br />'
        html += content
        html += u'</td></tr><tr style="background: #F2F2F2"><td colspan="2" style="padding: 10px 0 10px 25%; border-top: 1px solid #ccc; border-bottom: 1px solid #ccc;">'
        html += '<a style="-webkit-transform: translateY(0); -webkit-transition: -webkit-transform .2s ease-out; -moz-transform: translateY(0); -moz-transition: -moz-transform .2s ease-out; transform: translateY(0); transition: -moz-transform .2s ease-out; position: relative; top: 0; background-image: -webkit-linear-gradient(#6389C1, #4369A1); background-image: -moz-linear-gradient(#6389C1, #4369A1); background-image: -linear-gradient(#6389C1, #4369A1); height: 24px; box-shadow: rgba(0, 0, 0, 0.3) 2px 2px 5px 1px; border: 1px solid rgba(53, 85, 131, 0.9); border-radius: 2px; text-shadow: 0 1px rgba(0, 0, 0, 0.5); margin-top: 0px; cursor: pointer; font-size: 13px; font-family: Vavont, Helvetica, sans-serif; text-align: center; line-height: 20px; color: rgba(255, 255, 255, 0.99); box-sizing: border-box; margin-bottom: 5px; display: block; padding: 2px 6px 3px; overflow: hidden; text-decoration: none;width:70px;" href="'
        html += self.smtp_config.SITE_URL
        html += u'/diary/'
        html += str(did)
        html += u'/'
        html += diary_title
        html += u'">返回原文</a></td></tr></tbody>'
        html += u'<tfoot><tr><td colspan="2" style="font-size:11px;color:#999;padding-top:20px;">Copyright &copy; 2012-2013 Dev_Blog 博客评论邮件提醒。 Written By Scen(he.kang@dev-engine.com)</td></tr></tfoot></table>'
        return html


    def send_error_email(self, title, error_log):
        sender = self.smtp_config.USER
        password = self.smtp_config.PASSWORD
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(title, "UTF-8")
        msg['From'] = sender
        msg['To'] = self.smtp_config.EMAIL
        part = MIMEText(str(error_log), 'html', _charset='UTF-8')
        msg.attach(part)

        server = smtplib.SMTP(self.smtp_config.SERVER, self.smtp_config.PORT)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, self.smtp_config.EMAIL, msg.as_string())
        server.quit()
