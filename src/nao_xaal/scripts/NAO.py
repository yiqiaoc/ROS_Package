#!/usr/bin/python

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

    def verifyPersonState(self):
        self.say()
        self.hear()

    def say(self, words):
        pub = rospy.Publisher('/speech', String, queue_size=10)
        rospy.loginfo(self.check_str)
        pub.publish(self.end_str)
    
    def hear(self):
        self.valideWords = words
        client = actionlib.SimpleActionClient('speech_vocabulary_action', SetSpeechVocabularyAction)
        client.wait_for_server()
        goal = SetSpeechVocabularyGoal(words = [self.check_str, self.end_str])
    
        client.send_goal(goal)
        client.wait_for_result()

        rospy.Subscriber("/word_recognized", WordRecognized, self.hearCallback)
        rospy.wait_for_service('start_recognition')
        start = rospy.ServiceProxy('start_recognition', Empty)
        start()

    def hearCallback(self, data):
        if self.end_str == data.words[0] : self.verifyState = 1
        self.verifyState = 2
        stop()

    def getVerifyState(self):
        return self.verifyState

    def resetVerifyState(self):
        self.verifyState = 0

