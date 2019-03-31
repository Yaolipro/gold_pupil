# -*- coding: utf-8 -*-

"""
@created on 2018/8/16
@author Yao Li
"""

import smtplib
from email.header import Header
from email.mime.text import MIMEText


class Email(object):

    def __init__(self, sender, password, host):
        self.sender = sender
        self.password = password
        self.host = host

    def send(self, receivers, subject, content):
        try:
            server = smtplib.SMTP()
            server.connect(self.host)
            server.login(self.sender, self.password)
            message = MIMEText(content, 'plain', 'utf-8')
            message['Subject'] = Header(subject, 'utf-8')
            message['From'] = self.sender
            message['To'] = ';'.join(receivers)
            server.sendmail(self.sender, receivers, message.as_string())
            server.close()
        except smtplib.SMTPException as e:
            raise e

