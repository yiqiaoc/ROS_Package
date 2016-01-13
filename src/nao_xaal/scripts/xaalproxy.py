#!/usr/bin/python

from xAAL.core import Engine
from xAAL.message import Message
import ujson as json
import sys
from xAAL import tools
from xAAL import config

class xAALProxy:

    def __init__(self):

        self.uuid = tools.getRandomUUID()
        print("My UUID is : %s" % self.uuid)
        
        self.app = Engine()


    def sendmsg(self, target, action):
        
        addr = tools.getConfigFileAddr(target)

        msg = Message()
        msg.setTargets(addr)
        msg.setDevtype('cli.experimental') # ?? todo
        msg.setMsgtype('request')
        msg.setAction(action)
        msg.setSource(uuid)
        msg.setCipher("")
        msg.setSignature()
        txt = {"header":msg.getHeader(), "body":msg.getBody()}
        data = json.encode(txt)
        self.app.getNetworkConnector().send(data)

    def recvmsg(self):

        data = app.getNetworkConnector().getData()
        return data
