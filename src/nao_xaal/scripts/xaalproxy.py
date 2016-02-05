#!/usr/bin/python

from xAAL.core import Engine
from xAAL.message import Message
from xAAL import tools
import ujson as json
import sys
import config

class xAALProxy:

    def __init__(self):

        self.uuid = tools.getRandomUUID()
        print("My UUID is : %s" % self.uuid)
        
        self.app = Engine()


    def sendmsg(self, target, action):
        
        addr = config.getConfigInfo(target, "xaaladdr")

        msg = Message()
        msg.setTargets([addr])
        msg.setDevtype('cli.experimental') # ?? todo
        msg.setMsgtype('request')
        msg.setAction(action)
        msg.setSource(self.uuid)
        msg.setCipher("")
        msg.setSignature()
        txt = {"header":msg.getHeader(), "body":msg.getBody()}
        data = json.encode(txt)
        self.app.getNetworkConnector().send(data)

    def recvmsg(self):

        data = self.app.getNetworkConnector().getData()
        return data

# simple test
if __name__ == '__main__':
    proxy = xAALProxy()
    proxy.sendmsg("shutterleft","up")
    proxy.sendmsg("shutterright","up")
