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
        while(raw_input("continu ? (Y/N)")=="Y"):
	    if(self.kinect.fallDetection()):
	        self.nao.say("detecter la chute")
	        self.nao.say("detecter la chute")
	        self.nao.moveToPerson()
	        self.nao.verifyPersonState(5)
	        if not self.nao.getVerifyState()%2:
	            self.nao.say("Ne t'inquiete pas, je vais demander a quelqu'un pour t'aider")
	            print "verifystate ", self.nao.getVerifyState()
	            self.scenario()
	            self.nao.response(0)
	            self.nao.say("merci d'etre venu")
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
        self.smartDeviceAction("lamp1", "on")
        self.smartDeviceAction("lamp2", "on")
        self.smartDeviceAction("lamp3", "on")
	self.nao.say("porte ouverte, volet remonte")
        self.smartDeviceAction("switch", "off")
	self.nao.say("j'ai eteint l'electricite")
        try:
            self.sendMail()
        except:
            print "mail send failed"
	self.nao.say("j'ai envoye le mail a vos proches")
        self.smartDeviceAction("mobilephone","inform", "msg", "J'ai detecte un probleme. Votre ami a fait un malaise. Venez l'aider.")
	self.nao.say("message vocal envoye")
        

    def smartDeviceAction(self, device, action, key=None, value=None):
        self.xaalproxy.sendmsg(device, action, key, value)


if __name__== '__main__':
    c = Controller()
    try:
        c.run()
    except KeyboardInterrupt:
        print "Program Quit"
