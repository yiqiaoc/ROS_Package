#!/usr/bin/python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from naoqi_bridge_msgs.msg import *
import actionlib
from std_srvs.srv import Empty
import time


class NAO:

    def __init__(self, controller):
        rospy.init_node('nao', anonymous=True)
        self.controller = controller
        self.check_str = "salut mon amis, ca va"
        self.verifyState = 0 # 0 no answer, 1 for good situation, 2 for bad situation
        
    def moveToPerson(self):
        # disable word recognition before walking        
        stop = rospy.ServiceProxy('stop_recognition',Empty)
        stop()
        
        rospy.wait_for_service('/body_stiffness/enable')
        stif_enable = rospy.ServiceProxy('/body_stiffness/enable', Empty)
        stif_enable()
        
        p = rospy.Publisher('cmd_vel', Twist)

        twist = Twist()
        twist.linear.x = 0.1

        rospy.loginfo("About to be moving forward!")
        for i in range(20):
            p.publish(twist)
            rospy.sleep(0.5)

        twist = Twist()
        rospy.loginfo("Stopping!")
        p.publish(twist)
        
        alife_disable = rospy.ServiceProxy('/nao_alife/disabled', Empty)
        
        alife_disable()
        rospy.loginfo("NAO moves to person")

    def verifyPersonState(self, timeout):
        rospy.loginfo("NAO will verify person state")
        self.say(self.check_str)
        self.response(timeout)

    def say(self, words):
        for i in range(1):
            pub = rospy.Publisher('/speech', String, queue_size=10)
            rospy.loginfo(words)
            pub.publish(words)
            rospy.sleep(5)
        
    
    def response(self, timeout):
        self.resetVerifyState()
        
        client = actionlib.SimpleActionClient('speech_vocabulary_action', SetSpeechVocabularyAction)
        client.wait_for_server()
        goal = SetSpeechVocabularyGoal(words = ["oui","non"])
    
        client.send_goal(goal)
        client.wait_for_result()

        rospy.Subscriber("/word_recognized", WordRecognized, self.hearCallback)
        rospy.wait_for_service('start_recognition')
        start = rospy.ServiceProxy('start_recognition', Empty)
        start()
        
        count = 0
        while(not self.verifyState):
            rospy.sleep(5)
            count += 1
            if(timeout != 0) and (count > timeout):
                rospy.loginfo("wait person response timeout")
                break
        
        stop = rospy.ServiceProxy('stop_recognition',Empty)
        stop()


    def hearCallback(self, data):
        print "class NAO hearCallback"
        print data.words
        print data.confidence_values
        if data.words[0] == "oui" and data.confidence_values[0] > 0.4 : 
            self.verifyState = 1
        else :
            self.verifyState = 2

    def getVerifyState(self):
        return self.verifyState

    def resetVerifyState(self):
        self.verifyState = 0

