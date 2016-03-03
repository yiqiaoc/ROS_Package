#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import config

class Mail:

    def __init__(self, text):
        self.fromaddr = config.getConfigInfo("NAO mail","compte")
        self.toaddr = config.getConfigInfo("Contact list","user1")
        self.msg = MIMEMultipart()
        self.msg['Subject'] = "Nao assistant : aide a la personne"
        self.msg['From'] = self.fromaddr
        self.msg['To'] = self.toaddr
        self.msg.attach(MIMEText(text))

    def sendMail(self):
        srv = config.getConfigInfo("Server SMTP", "server")
        self.s = smtplib.SMTP(srv) # 465,587)
        #self.s.ehlo()
        #self.s.starttls()
        #self.s.ehlo()
        #pwd = config.getConfigInfo("NAO mail", "pwd")
        #self.s.login(self.fromaddr, pwd)
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
