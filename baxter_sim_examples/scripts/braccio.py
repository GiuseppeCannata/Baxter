#!/usr/bin/env python

# ROS
import rospy

# Moveit
import moveit_commander
import moveit_msgs.msg

# Baxter 
import baxter_interface

# Messaggi
from geometry_msgs.msg import (
    Pose,
    Point,
    Quaternion,
)

# Others
from ik_request import ik_request


class Braccio(object):

    def __init__(self, limb):
        
        self._name = limb
        self._robot = moveit_commander.RobotCommander()
        self._limb  = moveit_commander.MoveGroupCommander(limb+"_arm")

        self._rs = baxter_interface.RobotEnable(baxter_interface.CHECK_VERSION)
        self._init_state = self._rs.state().enabled
        self._rs.enable()

        self._gripper = baxter_interface.Gripper(limb)
        self._name_joints = [limb+"_s0", 
                             limb+"_s1",  
                             limb+"_e0", 
                             limb+"_e1", 
                             limb+"_w0", 
                             limb+"_w1", 
                             limb+"_w2"]


    # Consente di:
    #        1. Settare la posizione da raggiunre nello spazio dei giunti
    #        2. Lo spostamento del braccio nella posizione di giunto specificata      
    def move_with_joints(self, list_joints):

        joints = list()

        for name in self._name_joints:
            joints.append(list_joints[name])
        
        self._limb.set_joint_value_target(joints)
        plan = self._limb.plan()
        rospy.sleep(1)
        self._limb.go(wait=True)
    
    # Consente di:
    #        1. Settare la posizione da raggiunre in punti cartesiani
    #        2. Lo spostamento del braccio nella posizione specificata
    def move_with_pose(self, pose):

        res = False
        joints = ik_request(self._name, pose, False)  #gli passiamo il body del messaggio

        if joints:
		self._limb.set_joint_value_target(joints)
		plan = self._limb.plan()  
		rospy.sleep(1)
		self._limb.go(wait=True)
		res = True     

        return res
    
    # Restituisce la posizione in coordinate cartesiane del gripper
    def get_endpoint_pose(self):

        pose = baxter_interface.Limb(self._name).endpoint_pose()
        return  Pose (position=Point(x = pose["position"].x, y = pose["position"].y, z = pose["position"].z),
                      orientation=pose["orientation"])
       
    # Consente di aprire il gripper
    def gripper_open(self):
        self._gripper.open()
        rospy.sleep(1)

    # Consente di chiudere il gripper
    def gripper_close(self):
        self._gripper.close()
        rospy.sleep(1)
    """
    def prova(self, pose):
        joints = ik_request(self._name, pose, False) 
        baxter_interface.Limb("right").move_to_joint_positions(joints)
    """


       
