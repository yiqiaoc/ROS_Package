#!/usr/bin/python

from mail import Mail
from kinect import Kinect
from NAO import NAO
from xaalproxy import xAALProxy

class Controller:
    
    def __init__(self):
        conf = Config(xaalDevices)
        kinect = Kinect()
        nao = NAO()
        xaalproxy = xAALProxy()

    def run(self):
        if(kinect.fallDetection()):
            nao.moveToPerson()
            nao.verifyPersonState()
            if self.waitPersonResponse(30): break
            self.scenario()
            self.sendMail()
            # while(!self.waitPersonResponse(0))
            # how to return to the begin of scenario todo

    def waitPersonResponse(self, timeout):
        count = 0
        nao.resetVerifyState()
        while !nao.getVerifyState():
            time.sleep(3)
            count += 1
            if (timeout!=0) and (count > timeout) : return False
        return nao.getVerifyState()%2
    
    def sendMail(self):
        link = self.webRTCaddress()
        topic = "nao_robot/camera/top/camera/image_raw"
        text = "please see the video from this address " + link
        text = text + " with topic name " + topic
        mail = Mail(text)
        mail.sendMail()

    def webRTCaddress(self):
        # how to get the right ip address todo
        return "localhost:8080"

    def senario(self):
        self.smartDeviceAction('kettle', 'off')
        self.smartDeviceAction('autodoor', 'on')

    def smartDeviceAction(self, device, action):
        xaalproxy.sendmsg(device, action)


if __main__=='__main__':
    c = Controller()
    c.run()
