#!/usr/bin/env python

#node to publish irsensor readings

import rospy
from std_msgs.msg import String
from IR6SensorModule import IR6SensorModule

def talker():
    pub = rospy.Publisher('irsensor/readings/', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(50) # 10hz
    irsensor = IR6SensorModule(18,23,24,25,8,7);
    while not rospy.is_shutdown():
#        hello_str = "hello world %s" % rospy.get_time()
        sensorReadings = irsensor.readSensor();
        rospy.loginfo(sensorReadings)
        pub.publish(sensorReadings)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

