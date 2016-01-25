#!/usr/bin/python

import rospy
import tf
import geometry_msgs.msg

class Kinect:

    def __init__(self):
        self.listener = tf.TransformListener()
        self.rate = rospy.Rate(0.5)
        self.distance = 1

    def fallDetection(self):
        while self.distance > 0.05:
            print "distance h of neck and hip ", self.distance
            try:
                (trans1, rot1) = self.listener.lookupTransform('/openni_depth_frame', '/neck_1', rospy.Time(0))
                (trans2, rot2) = self.listener.lookupTransform('/openni_depth_frame', '/left_hip_1', rospy.Time(0))
                self.distance = abs(trans1[2]-trans2[2])
            
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue

            self.rate.sleep()

        rospy.loginfo("Fall detected!")
        return True
