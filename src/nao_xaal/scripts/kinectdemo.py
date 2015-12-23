#!/usr/bin/python

import rospy
import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('tf_lookup_example')
    listener = tf.TransformListener()
    rate = rospy.Rate(0.5)

    while not rospy.is_shutdown():
        try:
            (trans1, rot1) = listener.lookupTransform('/openni_depth_frame', '/right_foot_1', rospy.Time(0))
            (trans2, rot2) = listener.lookupTransform('/openni_depth_frame', '/left_hip_1', rospy.Time(0))
            print "distance Z between right foot and left hip : "
            print trans1[2]-trans2[2]
            print "=================="
        
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rate.sleep()
