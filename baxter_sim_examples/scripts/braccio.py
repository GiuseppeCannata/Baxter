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
    Pose,        # http://docs.ros.org/lunar/api/geometry_msgs/html/msg/Pose.html
    Point,       # http://docs.ros.org/lunar/api/geometry_msgs/html/msg/Point.html
    Quaternion,  # http://docs.ros.org/lunar/api/geometry_msgs/html/msg/Quaternion.html
)

# Others
from ik_request import ik_request


class Braccio(object):

    def __init__(self, limb):
        
        self._name = limb   # Nome del braccio: left/right
        self._robot = moveit_commander.RobotCommander()  # Prendiamo l oggetto Baxter
        self._limb  = moveit_commander.MoveGroupCommander(limb+"_arm")   # Prendiamo l oggetto braccio specificandone quello che vogliamo

		# Abilitiamo il robot affinche possa essere utilizzato
        self._rs = baxter_interface.RobotEnable(baxter_interface.CHECK_VERSION)
        self._init_state = self._rs.state().enabled
        self._rs.enable()

		# Prendiamo l oggetto gripper
        self._gripper = baxter_interface.Gripper(limb)
		
		# Lista in cui sono contenuti i nomi dei gunti del braccio
        self._name_joints = [limb+"_s0", 
                             limb+"_s1",  
                             limb+"_e0", 
                             limb+"_e1", 
                             limb+"_w0", 
                             limb+"_w1", 
                             limb+"_w2"]

    """
    Consente di eseguire lo spostamento del braccio considerando gli angoli di giunto     
    
    :param list_joints: Lista degli angoli di giunto in cui si vuole spostare il braccio
    """
    def move_with_joints(self, list_joints):

        joints = list()

		# Prendiamo gli angoli di giunto cercandoli per nome e li salviamo in joints
        for name in self._name_joints:
            joints.append(list_joints[name])
        
		# Settiamo gli angoli di giunto in cui vogliamo che il braccio si posizioni
        self._limb.set_joint_value_target(joints)
		
		# Cerchiamo la traiettoria priva di ostacoli
        plan = self._limb.plan()
        rospy.sleep(1)
		
		# Una volta trovata la traiettoria priva di ostacoli il braccio viene spostato
        self._limb.go(wait=True)
    
    """
    Consente di eseguire lo spostamento del braccio nella pose (coordinate nello spazio) specificata
	
    :param pose: Posizione in coordinate cartesiane in cui si vuole posizionare il braccio. 
	         Le coordinate devono essere prese considerando il gripper
    """
    def move_with_pose(self, pose):

        res = False
		
		# Invochiamo la ik_request per trasformare le coordinate cartesiane in angoli di giunto
        joints = ik_request(self._name, pose, False)  

        if joints:
			self._limb.set_joint_value_target(joints)
			plan = self._limb.plan()  
			rospy.sleep(1)
			self._limb.go(wait=True)
			res = True     

        return res
    
    """
    Restituisce la posizione in coordinate cartesiane del gripper
	
	:return: posizione attuale del gripper
	:rtype: Il tipo ritorno è un Pose
    """
    def get_endpoint_pose(self):

        pose = baxter_interface.Limb(self._name).endpoint_pose()
        return  Pose (position=Point(x = pose["position"].x, y = pose["position"].y, z = pose["position"].z),
                      orientation=pose["orientation"])
					  
    """   
    Consente di aprire il gripper
    """
    def gripper_open(self):
        self._gripper.open()
        rospy.sleep(1)
    
    """
    Consente di chiudere il gripper
    """
    def gripper_close(self):
        self._gripper.close()
        rospy.sleep(1)



       
