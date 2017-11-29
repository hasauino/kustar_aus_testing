cmake_minimum_required(VERSION 2.8.3)
project(kustar_aus_testing)



find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
  tf
)




catkin_package( 

CATKIN_DEPENDS 
)





include_directories(include ${catkin_INCLUDE_DIRS})


