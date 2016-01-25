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
        self.msg['Subject'] = "Nao assistant : aide a la personne"
        self.msg['From'] = me
        self.msg['To'] = you

    def sendMail(self):
        self.s = smtplib.SMTP(srv,587)
        self.s.ehlo()
        self.s.starttls()
        self.s.ehlo()
        self.s.login(me, pwd)
        self.s.sendmail(me, you, self.msg.as_string())
        self.s.quit()


# unit test
if __name__ == '__main__':
    link = "localhost:8080"
    topic = "nao_robot/camera/top/camera/image_raw"
    text = "please see the video from this address " + link
    text = text + " with topic name " + topic
    mail = Mail(text)
    mail.sendMail()
