#!/usr/bin/python

import rospy
import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('tf_lookup_example')
    listener = tf.TransformListener()
    rate = rospy.Rate(0.2)

    while not rospy.is_shutdown():
        try:
            (trans1, rot1) = listener.lookupTransform('/openni_depth_frame', '/neck_1', rospy.Time(0))
            (trans2, rot2) = listener.lookupTransform('/openni_depth_frame', '/left_hip_1', rospy.Time(0))

            print "distance X between neck and left hip : "
            print trans1[0] - trans2[0]
            print "distance Y between neck and left hip : "
            print trans1[1] - trans2[1]
            print "distance z between neck and left hip : "
            print trans1[2] - trans2[2]
            print "=================="
        
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rate.sleep()
