#!/usr/bin/env python

# ROS
import rospy
# Messaggi
from geometry_msgs.msg import (
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Bool
import baxter_interface

def talker(name_topic, tipo_messaggio, size_coda, msg):

       pub = rospy.Publisher(name_topic, tipo_messaggio, queue_size=size_coda)

       rospy.loginfo("Invio messaggio in corso..")
       rospy.loginfo(msg)

       rospy.sleep(1)
       pub.publish(msg)
       rospy.loginfo("Ho pubblicato")
        

def listener(name_topic, tipo_messaggio, function):
       rospy.Subscriber(name_topic, tipo_messaggio, function) 
