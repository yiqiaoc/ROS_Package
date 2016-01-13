#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText

me = "naorobot@hotmail.com"
you = "yiqiaoc@hotmail.com"
pwd = "mynao1234"
srv = "smtp.live.com"

class Mail:

    def __init__(self, text):
        self.msg = MIMEText(text)
        self.msg['Subject'] = "Nao assistant : aide à la personne"
        self.msg['From'] = me
        self.msg['To'] = you

    def sendMain(self):
        s = smtplib.SMTP(srv,587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(me, pwd)
        s.sendmail(me, you, msg.as_string())
        s.quit()
