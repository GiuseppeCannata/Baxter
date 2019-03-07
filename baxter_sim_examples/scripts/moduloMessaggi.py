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

"""
Permette di scrivere un messaggio sul topic specificato

:param name_topic: nome del topic sul quale si vuole scrivere
:param tipo_messaggio: tipo del messaggio che scriviamo sul topic
:param size_coda: lunghezza del buffer del topic
:param msg: messaggio 
"""
def talker(name_topic, tipo_messaggio, size_coda, msg):

       pub = rospy.Publisher(name_topic, tipo_messaggio, queue_size=size_coda)

       rospy.loginfo("Invio messaggio in corso..")
       rospy.loginfo(msg)

       rospy.sleep(1)
       pub.publish(msg)
       rospy.loginfo("Ho pubblicato
	   
        
"""
Permette di scrivere un messaggio sul topic specificato

:param name_topic: nome del topic da cui vogliamo leggere
:param tipo_messaggio: tipo del messaggio che vogliamo leggere
:param function: funzione da applicare al messaggio che leggiamo
"""
def listener(name_topic, tipo_messaggio, function):
       rospy.Subscriber(name_topic, tipo_messaggio, function) 
