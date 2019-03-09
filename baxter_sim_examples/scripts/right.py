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


def right():

    rospy.init_node("right_arm")  # Iniziallizziamo il nodo ROS
    r_braccio = Braccio("right")  # Istanziamo la classe Baxter passandogli il nome

    # Attende che il sinistro abbia trovato il punto di scambio
    data = rospy.wait_for_message("left/msg", Pose, timeout=None)
    r_braccio.gripper_open()
	
    # PRIMO PUNTO DI ARRIVO
    start1 = Pose( position= Point(x=0.0511116965597, y=-0.864422194945, z=-0.305731378478),
                 orientation= Quaternion(x=0.471615536924, y=0.881779971596, z=-0.00562827161274, w=-0.00334508327601))
    r_braccio.move_with_pose(start1)
    rospy.sleep(1)
	
    # SECONDO PUNTO DI ARRIVO
    start2 = Pose( position= Point(x=0.469330967229, y=-0.55023988915, z=0.404403189229),
                 orientation= Quaternion(x=0.471577579986, y=0.881800825784, z=-0.00558788488991, w=-0.00326576857884))
    r_braccio.move_with_pose(start2)
    rospy.sleep(1)
	
    # TERZO PUNTO DI ARRIVO
    starting_joint_angles = {'right_w0': 1.4337025470874254,
                             'right_w1': 1.6612876079132552,
                             'right_w2': -1.4625539596386004,
                             'right_e0': -0.021239405634914554,
                             'right_e1': 1.7468265340113902,
                             'right_s0': 0.6213823436317725,
                             'right_s1': -0.3642896913230187}
    r_braccio.move_with_joints(starting_joint_angles)
    
	
    # Spostiamo il braccio nella posizione indicata dal braccio sinistro
    data.position = Point(x= 0.585560666885, y= 0.209368041126, z= 0.105)
    data.orientation = Quaternion(x=-0.01508949187, y= 0.705381077844, z= 0.707937222017, w= 0.032167249461)
    rospy.sleep(1)
    r_braccio.move_with_pose(data)
    rospy.sleep(1)
	
    # Afferriamo il pezzo
    r_braccio.gripper_close() 

    # Diciamo al braccio sinistro di aver preso il pezzo
    talker("right/msg", Bool, 1, True)
	
    # Attendiamo che il braccio sinistro abbia aperto il gripper
    # data == True il gripper e aperto
    data = rospy.wait_for_message("left1/msg", Bool, timeout=None)

    if data:
	
       # Punto intermedio 1 (sotto il gripper sx)
       int1 = Pose( position= Point(x=0.59646481601, y=0.256599564965, z=-0.0152786373748),
                 orientation= Quaternion(x=-0.00553449776039, y=0.698224446563, z=0.712501515165, w=0.0692357020905))
       r_braccio.move_with_pose(int1)
       rospy.sleep(1)
	   
       # Punto intermedio 2 
       int2 = Pose( position= Point(x=0.597068370528, y=-0.0457122506092, z=0.00175406270759),
                 orientation= Quaternion(x=-0.00562289135545, y=0.698260045752, z=0.712471697084, w=0.0691763865266))
       r_braccio.move_with_pose(int2)
       rospy.sleep(1)

       # QUARTO PUNTO DI ARRIVO
       final_joint_angles = {'right_w0': 1.4536034401562068,
                             'right_w1': 1.3508498030339906,
                             'right_w2': -1.380729984871202,
                             'right_e0': -0.021277518545398166,
                             'right_e1': 2.0672138937713527,
                             'right_s0': 0.6330501993545647,
                             'right_s1': -0.788209869979708}
       r_braccio.move_with_joints(final_joint_angles)
       talker("right1/msg", Bool, 1, True)
    
if __name__ == '__main__':
    right()

