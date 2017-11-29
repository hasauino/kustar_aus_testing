#!/usr/bin/env python

#--------Include modules---------------
import rospy
import tf
from tf2_msgs.msg import TFMessage
from time import sleep

def callBack(data):
	global static_tf_tree
	static_tf_tree[data.transforms[0].child_frame_id]=data.transforms[0]



static_tf_tree={}
rospy.init_node('static_tf_republisher', anonymous=False) 
rate = rospy.Rate(100)
rospy.Subscriber('/tf_static', TFMessage, callBack)
br=tf.TransformBroadcaster()


while not rospy.is_shutdown():
	for frame in static_tf_tree:
		translation=(static_tf_tree[frame].transform.translation.x,static_tf_tree[frame].transform.translation.y,static_tf_tree[frame].transform.translation.z)
		rotation=(static_tf_tree[frame].transform.rotation.x,static_tf_tree[frame].transform.rotation.y,static_tf_tree[frame].transform.rotation.z,static_tf_tree[frame].transform.rotation.w)
		br.sendTransform(translation, rotation, rospy.Time.now(), static_tf_tree[frame].child_frame_id, static_tf_tree[frame].header.frame_id)
	rate.sleep() 

