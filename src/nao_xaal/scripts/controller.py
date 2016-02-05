#!/usr/bin/python

from mail import Mail
from kinect import Kinect
from NAO import NAO
from xaalproxy import xAALProxy
import netifaces as ni
import time

class Controller:
    
    def __init__(self):
        self.nao = NAO(self)
        self.kinect = Kinect()
        self.xaalproxy = xAALProxy()

    def run(self):
        print "====run===="
        #while(1):
        if(self.kinect.fallDetection()):
            self.nao.say("detecter la chute")
            self.nao.moveToPerson()
            self.nao.verifyPersonState(5)
            if not self.nao.getVerifyState()%2:
                self.nao.say("Ne t'inquiete pas, je vais demander à quelqu'un pour t'aider")
                print "verifystate ", self.nao.getVerifyState()
                self.scenario()
                self.nao.say("porte ouverte, volet remonte")
                self.sendMail()
                self.nao.say("mail envoye")
                # TODO last valide action to be defined
                self.nao.response(0)
                self.nao.say("merci d'être venu")
            else :
                self.nao.say("tres bien")
                

    def waitPersonResponse(self, timeout):
        count = 0
        self.nao.resetVerifyState()
        while not self.nao.getVerifyState():
            time.sleep(3)
            count += 1
            if (timeout!=0) and (count > timeout) : 
                print "waitpersonresponse timeout!"
                return False
        print "getpersonresponse"
        return self.nao.getVerifyState()%2
    
    def sendMail(self):
        link = self.webRTCaddress()
        topic = "nao_robot/camera/top/camera/image_raw"
        text = "please see the video from this address " + link
        text = text + " with topic name " + topic
        mail = Mail(text)
        mail.sendMail()

    def webRTCaddress(self):
        ni.ifaddresses('wlan0')
        ip = ni.ifaddresses('wlan0')[2][0]['addr'] + ":8080"
        print "HostIP : ", ip
        return ip

    def scenario(self):
        self.smartDeviceAction("shutterleft", "up")
        self.smartDeviceAction("shutterright", "up")

    def smartDeviceAction(self, device, action):
        self.xaalproxy.sendmsg(device, action)


if __name__== '__main__':
    c = Controller()
    try:
        c.run()
    except KeyboardInterrupt:
        print "Program Quit"
