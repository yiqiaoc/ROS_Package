#!/usr/bin/python

import rospy
import tf
import geometry_msg.msg

class kinect:

    def __init__(self):
        self.listener = tf.TransformListener()
        self.rate = rospy.Rate(0.5)
        self.distance = 1

    def fallDetection(self):
        while self.distance:
            try:
                (trans1, rot1) = listener.lookupTransform('/openni_depth_frame', '/right_foot_1', rospy.Time(0))
                (trans2, rot2) = listener.lookupTransform('/openni_depth_frame', '/left_hip_1', rospy.Time(0))
                self.distance = trans1[2]-trans2[2]
            
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue

            rate.sleep()

        return True
