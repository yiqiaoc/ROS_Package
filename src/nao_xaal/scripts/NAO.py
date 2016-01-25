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
        self.end_str = "c'est pas grave"
        self.verifyState = 0 # 0 no answer, 1 for good situation, 2 for bad situation
        
    def moveToPerson(self):
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

    def verifyPersonState(self):
        self.say()
        #self.hear()

    def say(self):
        for i in range(5):
            pub = rospy.Publisher('/speech', String, queue_size=10)
            rospy.loginfo(self.check_str)
            pub.publish(self.check_str)
            print "NAO say sth"
            rospy.sleep(5)
        
    
    def hear(self):
        client = actionlib.SimpleActionClient('speech_vocabulary_action', SetSpeechVocabularyAction)
        client.wait_for_server()
        goal = SetSpeechVocabularyGoal(words = [self.end_str])
    
        client.send_goal(goal)
        client.wait_for_result()

        rospy.Subscriber("/word_recognized", WordRecognized, self.hearCallback)
        rospy.wait_for_service('start_recognition')
        start = rospy.ServiceProxy('start_recognition', Empty)
        start()

    def hearCallback(self, data):
        print "class NAO hearCallback"
        print data.words
        print data.confidence_values
        if data.confidence_values[0] > 0.5 : self.verifyState = 1
        self.verifyState = 2
        stop = rospy.ServiceProxy('stop_recognition',Empty)
        stop()

    def getVerifyState(self):
        return self.verifyState

    def resetVerifyState(self):
        self.verifyState = 0

