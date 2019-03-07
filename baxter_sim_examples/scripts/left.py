#! /usr/bin/env python

# ROS
import rospy

# Moveit
import moveit_commander
import moveit_msgs.msg

# Messaggi
from geometry_msgs.msg import (
    Pose,        # http://docs.ros.org/lunar/api/geometry_msgs/html/msg/Pose.html
    Point,       # http://docs.ros.org/lunar/api/geometry_msgs/html/msg/Point.html
    Quaternion,  # http://docs.ros.org/lunar/api/geometry_msgs/html/msg/Quaternion.html
)
from std_msgs.msg import Bool

# Others
from braccio import Braccio 
from moduloMessaggi import ( 
    listener, 
    talker,
)


def left():

    rospy.init_node("left_arm") # Iniziallizziamo il nodo ROS
    l_braccio = Braccio("left")  # Istanziamo la classe Baxter passandogli il nome
	
    # PRIMO PUNTO DI ARRIVO del braccio sinistro
    start1L = Pose( position= Point(x=0.209535215152, y=0.605063524198, z=-0.464342360685),
                 orientation= Quaternion(x=-0.558752963108, y=0.829306297467, z=-0.00550209787199, w= 0.00398975170912))
    l_braccio.move_with_pose(start1L)
    rospy.sleep(1)
	
	# SECONDO PUNTO DI ARRIVO del braccio sinistro
    starting_joint_angles = {'left_w0': 0.6699952259595108,
                             'left_w1': 1.030009435085784,
                             'left_w2': -0.4999997247485215,
                             'left_e0': -1.189968899785275,
                             'left_e1': 1.9400238130755056,
                             'left_s0': -0.08000397926829805,
                             'left_s1': -0.9999781166910306}
    l_braccio.move_with_joints(starting_joint_angles)
	
	# Apriamo il gripper
    l_braccio.gripper_open()

    # Forniamo le posizioni del blocchetto
    pose = Pose( position= Point(x=0.7, y=0.155, z=-0.1325),
                 orientation= Quaternion(x=-0.02495908, y=0.999649, z=0.00737916, w=0.0048645))
    
	# Spostiamo il braccio
    if l_braccio.move_with_pose(pose):
  
		l_braccio.gripper_close()  # Afferriamo il blocchetto
		l_braccio.move_with_joints(starting_joint_angles) # Ci spostiamo nel secondo punto di arrivo
		  
		# TERZO PUNTO DI ARRIVO: Ruotiamo il gripper
		pose = l_braccio.get_endpoint_pose() 
		pose.orientation = Quaternion(x= 0.709767506221, y= 0.703906440537 , z= 0.022870575989 , w= 0.0149247056287)
		
		if l_braccio.move_with_pose(pose):

			try:
				 
				# Inviamo la posizione del gripper al braccio destro
				talker("left/msg", Pose, 1, pose)
			
				# Attendiamo che il braccio raggiunga il blocchetto
				# data == True allora il braccio destro l avrà raggiunto
				data = rospy.wait_for_message("right/msg", Bool, timeout=None)

				if data:
					l_braccio.gripper_open() # Apriamo il gripper per consentire al braccio destro di prendere il pezzo
					rospy.sleep(2)
					
					# Diciamo al braccio destro di aver aperto il gripper
					talker("left1/msg", Bool, 1, True)
					
					# Attendiamo che il braccio destro afferri il pezzo
					# data == True allora il braccio destro avrà preso il pezzo
					data = rospy.wait_for_message("right1/msg", Bool, timeout=None) 

					if data:
						# Spostiamo il braccio sinistro nella terza posizione
						l_braccio.move_with_joints(starting_joint_angles)
					 

			except rospy.ROSInterruptException:
				pass  
				
        else:
            rospy.logerr("No Joint Angles provided for move_to_joint_positions. Staying put.")
    else:
        rospy.logerr("No Joint Angles provided for move_to_joint_positions. Staying put.")  


if __name__ == '__main__':
    left()



