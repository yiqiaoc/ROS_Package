#!/usr/bin/python

from mail import Mail
from kinect import Kinect
from NAO import NAO
from xaalproxy import xAALProxy
import time

class Controller:
    
    def __init__(self):
        # TODO class config
        # self.conf = Config(xaalDevices)
        self.nao = NAO(self)
        raw_input("after self.nao = NAO(self)")
        self.kinect = Kinect()
        raw_input("after self.kinect = Kinect()")
        self.xaalproxy = xAALProxy()
        raw_input("after self.xaalproxy = xAALProxy()")

    def run(self):
        print "====run===="
        #if(self.kinect.fallDetection()):
        if(True):
            raw_input("kinect detecte fall")
            self.nao.moveToPerson()
            raw_input("nao move to person")
            self.nao.verifyPersonState()
            raw_input("nao verifypersonstate")
            if not self.waitPersonResponse(10): 
                raw_input("person response negatif")
                self.scenario()
                raw_input("control samrt devices")
                self.sendMail()
                raw_input("mail sended")
                # while(!self.waitPersonResponse(0))
                # how to return to the begin of scenario todo

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
        # TODO how to get the right ip address todo
        import netifaces as ni
        ni.ifaddresses('wlan0')
        ip = ni.ifaddresses('wlan0')[2][0]['addr']
        print "HostIP : ", ip
        return ip

    def scenario(self):
        self.smartDeviceAction("shutterleft", "down")
        self.smartDeviceAction("shutterright", "up")

    def smartDeviceAction(self, device, action):
        self.xaalproxy.sendmsg(device, action)


if __name__== '__main__':
    c = Controller()
    c.run()
