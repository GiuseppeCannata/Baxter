<h1> Baxter </h1>
<p>
La robot application è stata realizzata come progetto per il corso di misure e strumentazione per l'utomazione presso il laboratorio di robotica dell'università politecnica della marche.
L'obiettivo era quello di effettuare lo scambio di un oggetto tra il gripper del braccio sinistro e il gripper del braccio destro.
Lo scambio può avvenire in condizioni sia di assenza sia di presenza di ostacoli. In quest'ultimo caso il robot deve evitare l'ostacolo trovando la traiettoria opportuna.

La robot application è stata realizzata utilizzando il framework ROS e il modello del baxter fornito da RethinkRobotics.
I tool utilizzati sono:
<br>
<ul> 
  <li> <b>Gazebo:</b> simulatore </li>
  <li> <b>RViz:</b> per visualizzare gli ostacoli e muovere il modello del baxter senza l'utilizzo di joystick </li>
  <li> <b>Moveit:</b> libreria che ci ha permesso di trovare la traiettoria dei bracci considerando la presenza di ostacoli </li>
</ul>
</p>
<br>
<h3> - Utilizzo del sorgente </h3>
<p>
La cartella baxter_sim_examples è un package ROS, per poterlo utilizzare seguire i seguenti passi:
<ol> 
  <li> Scaricare la cartella e spostarla nella cartella src del proprio WorkSpace. Dopodichè ricompilare il Workspace facendo catkin_make   </li>
  <li> Rendere i file eseguibili; Per farlo eseguire:  
       <ol>
	    <li> roscd baxter_project </li>
		<li> cd scripts </li>
		<li> sudo chmod +x ./*.py </li>
	   </ol>
  </li>
  <li> Aprire un terminale, avviare Gazebo ed attendere il termine del caricamento  </li>
  <li> Aprire un ulteriore terminale e attivare il robot eseguendo il seguente comando: rosrun baxter_tools enable_robot.py -e
       <br>
       Nello stesso terminale eseguire il comando: rosrun baxter_interface joint_trajectory_action_server.py
  </li>
  <li> Aprire un ulteriore terminale ed avviare RViz: roslaunch baxter_moveit_config baxter_grippers.launch</li>
  <li> Aprire un ulteriore terminale ed eseguire: rosrun baxter_project right.py </li>
  <li> Aprire un ulteriore terminale ed eseguire: rosrun baxter_project left.py </li>
</ol>
</p>
