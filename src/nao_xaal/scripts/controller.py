#!/usr/bin/python

from mail import Mail
from kinect import Kinect
from NAO import NAO
from xaalproxy import xAALProxy
import netifaces as ni
import time

class Controller:
    
    def __init__(self):
        # TODO class config
        # self.conf = Config(xaalDevices)
        self.nao = NAO(self)
        self.kinect = Kinect()
        self.xaalproxy = xAALProxy()

    def run(self):
        print "====run===="
        while(1):
        #if(self.kinect.fallDetection()):
            self.nao.moveToPerson()
            self.nao.verifyPersonState(5)
            if not self.nao.getVerifyState()%2: 
                self.scenario()
                self.sendMail()
                # TODO last valide action to be defined
                self.nao.response(0)
                

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
    except KeyboardInterrput:
        print "Program Quit"
