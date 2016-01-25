#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText
import config

class Mail:

    def __init__(self, text):
        self.fromaddr = config.getConfigInfo("NAO mail","compte")
        self.toaddr = config.getConfigInfo("Contact list","user1")
        self.msg = MIMEText(text)
        self.msg['Subject'] = "Nao assistant : aide a la personne"
        self.msg['From'] = self.fromaddr
        self.msg['To'] = self.toaddr

    def sendMail(self):
        self.s = smtplib.SMTP(srv,587)
        self.s.ehlo()
        self.s.starttls()
        self.s.ehlo()
        pwd = config.getConfigInfo("NAO mail", "pwd")
        self.s.login(self.fromaddr, pwd)
        self.s.sendmail(self.fromaddr, self.toaddr, self.msg.as_string())
        self.s.quit()


# unit test
if __name__ == '__main__':
    link = "localhost:8080"
    topic = "nao_robot/camera/top/camera/image_raw"
    text = "please see the video from this address " + link
    text = text + " with topic name " + topic
    mail = Mail(text)
    mail.sendMail()
