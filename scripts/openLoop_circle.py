#!/usr/bin/env python

#--------Include modules---------------
import rospy
import tf
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from numpy import arange,pi,cos,sin
import matplotlib.pyplot as plt
from time import sleep

rospy.init_node('openLoop_circle', anonymous=False) 	#initalizes the node
rate = rospy.Rate(100)	#loop rate in Hz
pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)	#publisher to send velocity commands, msg type is Twist
pub_reset_odom = rospy.Publisher('/mobile_base/commands/reset_odometry', Empty, queue_size=10)	#publisher to to reset theodometry
tfLisn=tf.TransformListener()	#using this class we can get robot's pose
tfLisn.waitForTransform('/odom', '/base_footprint', rospy.Time(0),rospy.Duration(10.0)) #wait to make sure pose data are ready

#reseting odometry of the robot
sleep(0.1)
res_msg=Empty()
pub_reset_odom.publish(res_msg)
sleep(0.1)

#our velocity msg. Tyoe of the msg is Twist
msg=Twist()


#----------------------------------------------------------------------

r=5.0	#radius of circular path
v=0.1	#robot speed
w=v/r


#Plotting------------------------------------------------
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
t=arange(0,2*pi,0.1)
y=r*cos(t)+r  #actually it should be x=r*cos(t)+r. But, for kobuki x is forward, for the plot y is the forward (axes are flipped, y is and x is y)
x=r*sin(t)
line1,line2,line3 = ax.plot(x, y, 'b--',0,0,'r-',0,0,'k*')
ax.set_xlim(-r-2, r+2)
ax.set_ylim(-2, 2*r+2)
ax.grid()
X2=[]
Y2=[]


# Main Loop
while not rospy.is_shutdown():
	position=tfLisn.lookupTransform('/odom', '/base_footprint', rospy.Time(0))[0]
	msg.linear.x=v
	msg.angular.z=w
	pub.publish(msg)

#plotting
	X2+=[position[0]]
	Y2+=[position[1]]
	line3.set_xdata(position[0])
	line3.set_ydata(position[1])
	
	line2.set_ydata(Y2)
	line2.set_xdata(X2)
	fig.canvas.draw()
	
	rate.sleep()  #calling this function ensures the previously specified loop rate is achieved (if possible)



