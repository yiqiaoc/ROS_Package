#!/usr/bin/python

import rospy
from std_srvs.srv import Empty

def stiffness():
    rospy.init_node('stiffness', anonymous=True)
    rospy.wait_for_service('/body_stiffness/enable')
    print "after wait for service"
    try:
        enable = rospy.ServiceProxy('/body_stiffness/enable', Empty)
        disable = rospy.ServiceProxy('/body_stiffness/disable', Empty)
        enable()
        # disable()   
    except rospy.ServiceException, e:
        print "Service call failed : %s" %e

if __name__ == '__main__':
    try:
        stiffness()
    except rospy.ROSInterruptException:
        pass
