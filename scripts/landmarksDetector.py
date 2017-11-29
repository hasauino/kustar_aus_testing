#!/usr/bin/env python
import cv2
import rospy
from ar_markers import detect_markers
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import PointCloud2
from sensor_msgs.point_cloud2 import read_points
from cv_bridge import CvBridge, CvBridgeError
from time import sleep
import numpy as np
import tf
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import PointStamped
from std_msgs.msg import String


#Call back functions (Handling subscribed data)
def callBack(data):
	global img
	img=data

def callBack2(data):
	global info
	info=data

def callBack3(data):
	global pointCloud
	pointCloud=data
	

	

rospy.init_node('landmarksDetector', anonymous=False)
rate = rospy.Rate(30)

point=PointStamped()
transformed_point=PointStamped()
img=Image()
pointCloud=PointCloud2()
info=CameraInfo()
bridge = CvBridge()


rospy.Subscriber('/camera/rgb/image_color', Image, callBack)
rospy.Subscriber('/camera/depth_registered/points', PointCloud2, callBack3)
rospy.Subscriber('/camera/rgb/camera_info', CameraInfo, callBack2)

msg_names=String()
pub = rospy.Publisher('available_LandMarks', String, queue_size=10)


transformer=tf.TransformerROS()
transformer2=tf.Transformer()
listener=tf.TransformListener()
br=tf.TransformBroadcaster()


while img.header.seq<1:
	pass
	

while pointCloud.header.seq<1:
	pass

while info.header.seq<1:
	pass




while not rospy.is_shutdown():

	frame = bridge.imgmsg_to_cv2(img, desired_encoding="passthrough")
	markers = detect_markers(frame)
	
	point.header=img.header

	msg_names.data=''
	for marker in markers:
			marker.highlite_marker(frame)
			id_Marker=marker.id
			center=marker.center	#center[0] is x in pixels. center[1] is y in pixles
			
			if len(msg_names.data)>0:
				msg_names.data=msg_names.data+','+str(id_Marker)
			else:
				msg_names.data=str(id_Marker)
			print 'Landmark ',id_Marker,' detected'
			
			fields=list(read_points(pointCloud, skip_nans=False, field_names=("x", "y", "z"), uvs=[center]))
			

			if len(fields[0])>0:
				br.sendTransform((fields[0][0],fields[0][1],fields[0][2]), (0,0,0,1), rospy.Time.now(), 'landMark_'+str(id_Marker), img.header.frame_id)

	pub.publish(msg_names)
	#cv2.circle(frame, (info.width/2,info.height/2), 20, (100,100,100))	
		
	


	cv2.imshow('Test Frame', frame)
	cv2.waitKey(10)

	rate.sleep()

