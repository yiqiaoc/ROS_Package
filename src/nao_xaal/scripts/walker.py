#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist

if __name__=="__maiin__":

    rospy.init_node('move')

    p = rospy.Publisher('cmd_vel', Twist)

    twist = Twist()
    twist.linear.x = 1.0
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0

    rospy.loginfo("About to be moving forward!")
    for i in range(10):
        p.publish(twist)
        rospy.sleep(0.1)

    twist = Twist()
    rospy.loginfo("Stopping!")
    p.publish(twist)
