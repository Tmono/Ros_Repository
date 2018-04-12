#!/usr/bin/env python
import roslib; roslib.load_manifest('keyboard_target')
import rospy
import math
import tf
import os

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Point
from threading import Thread  

import sys, select, termios, tty

msg = """ Moving Around:
q/Q top right w/W upward    e/E top left
a/A left      s/S backward  d/D right
z/Z back left d/D right     c/C back right
------------------------------------------
Ctrl+C Exit"""

moveBindings = {
		'q':(-1,1), # top right
		'w':(0,1),# upward
		'e':(1,1), # top left
		'a':(-1,0), # left
		's':(0,-1),  # backward
		'd':(1,0), # right
		'z':(-1,-1), # back left
		'c':(1, -1), # back right
		
		'Q':(-1,1), # top right
		'W':(0,1),# upward
		'E':(1,1), # top left
		'A':(-1,0), # left
		'S':(0,-1),  # backward
		'D':(1,0), # right
		'Z':(-1,-1), # back left
		'C':(1, -1), # back right
	       }
goal_x = 0.
goal_y = 0.
state_ = 0 # 0 is tracking 1 is stop
res = 0

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0.001)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


def publisher():	
	try:
		Goal = PoseStamped()
		Goal.header.stamp = rospy.get_rostime()
		Goal.header.frame_id = target_frame
		Goal.pose.position.x = goal_x
		Goal.pose.position.y = goal_y
		Goal.pose.position.z = 0.
		quat = tf.transformations.quaternion_from_euler(0, 0, math.atan2(goal_x, goal_y))
		Goal.pose.orientation.x = quat[0]
		Goal.pose.orientation.y = quat[1]
		Goal.pose.orientation.z = quat[2]
		Goal.pose.orientation.w = quat[3]

		pub_goal.publish(Goal)

		State = PoseStamped()
		State.header.stamp = rospy.get_rostime()
		State.header.frame_id = target_frame
		State.pose.position.x = state_
		State.pose.position.y = 0.
		State.pose.position.z = 0.

		pub_state.publish(State)

	except Exception as e:
		print e
		
def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0.001)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

def useKey():
	global res
	global goal_x, goal_y, state_, goal_x_default, goal_y_default
	while(1):
		key = getKey()
		if key in moveBindings.keys():
			state_ = 0
			goal_x += moveBindings[key][0]*speed
			goal_y += moveBindings[key][1]*speed
		elif key == 'r' or key == "R":
			state_ = 0
			goal_x = goal_x_default
			goal_y = goal_y_default
		elif key == 't' or key == 'T':
			goal_x = goal_x_default
			goal_y = goal_y_default
			state_ = 1
		else:
			state_ = 0
		if (key == '\x03'):
			goal_x = 0.
			goal_y = 0.
			state = 1
			res = -1
			break
			
		if state_ == 0:
			print ("Tracking")
		else:
			print ("Lost")
		print ("Goal is (%f, %f)" %(goal_x,goal_y))
	if res == -1:
		try:  
			os._exit(0)  
		except:  
			print('ByeBye.')  

class KeyboardThread(Thread):
	def __init_(self):
		super(KeyboardThread, self).__init__()
		
	def run(self):
		useKey()
	
	

if __name__=="__main__":
	settings = termios.tcgetattr(sys.stdin)
	

	pub_goal = rospy.Publisher('fusion_target', PoseStamped, queue_size = 1)
	pub_state = rospy.Publisher('single_cam_tracker_state', PoseStamped, queue_size = 1)

	rospy.init_node('keyboard_target')
	
	
	target_frame = rospy.get_param("~target_frame", "base_frame") # frame_id
	speed = rospy.get_param("~internal", 0.4) # meter
	goal_x_default = rospy.get_param("~goal_x", 0.0) # meter
	goal_y_default = rospy.get_param("~goal_y", 0.0) # meter
	goal_x = goal_x_default
	goal_y = goal_y_default
	
	rate = rospy.Rate(30)	

	try:
		print (msg)
		
		input_ = KeyboardThread()
		input_.start()
		while(1):
			publisher()
			rate.sleep()
			
	except Exception as e:
		print (e)

	finally:
		if state_ == 0:
			print ("Tracking")
		else:
			print ("Lost")
		print ("Goal is (%f, %f)" %(goal_x,goal_y))
		
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


