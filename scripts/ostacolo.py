#! /usr/bin/env python

# ROS
import rospy

# Moveit
import moveit_commander

# Messaggi
from geometry_msgs.msg import (
    PoseStamped
)


if __name__ == '__main__':
  
   rospy.init_node("ostacolo")
   scene = moveit_commander.PlanningSceneInterface()
   rospy.sleep(2)

   # Creazione ostacolo
   ostacolo = PoseStamped()
   ostacolo.header.frame_id = "world"
   ostacolo.pose.position.x = 0.7
   ostacolo.pose.position.y = 0.01
   ostacolo.pose.position.z = -0.59
   
   # 1 param: nome dell ostacolo
   # 2 param: ostacolo
   # 3 param: dimensioni ostacolo , profondita, lunghezza, altezza
   scene.add_box("table", ostacolo, (0.553756, 0.9, 0.7))

   # Creazione ostacolo
   ostacolo2 = PoseStamped()
   ostacolo2.header.frame_id = "world"
   ostacolo2.pose.position.x = 0.44  
   ostacolo2.pose.position.y = 0.25
   ostacolo2.pose.position.z = 0.0
  
   scene.add_box("pillar1", ostacolo2, (0.08964, 0.08964, 0.4482))

   """# Creazione ostacolo
   ostacolo3 = PoseStamped()
   ostacolo3.header.frame_id = "world"
   ostacolo3.pose.position.x = 0.44  
   ostacolo3.pose.position.y = -0.18
   ostacolo3.pose.position.z = 0.22

   ostacolo3.pose.orientation.x = -0.707387 
   ostacolo3.pose.orientation.y = 0.00112618
   ostacolo3.pose.orientation.z = 0.0
   ostacolo3.pose.orientation.w = 0.706825
 
   scene.add_box("pillar2", ostacolo3, (0.08964, 0.08964, 0.4482))"""
  
