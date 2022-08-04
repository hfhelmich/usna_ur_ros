#!/usr/bin/env python3


import time
#import roslib; roslib.load_manifest('ur_driver')
import rospy
import actionlib
import csv
import numpy
from control_msgs.msg import *
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
from math import pi
import codecs
import tkinter as tk
from tkinter import filedialog

client = None

JOINT_NAMES = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

rt = tk.Tk()
rt.withdraw()
file_path = filedialog.askopenfilename()
print(file_path)
sliceFile = open(file_path, "rb")
reader = csv.reader(codecs.iterdecode(sliceFile, 'utf-8'), delimiter=",") #open trajectory file
traj_list = list(reader) #open as a list
traj = numpy.array(traj_list).astype("float") #convert to float and store in a python array
rob = input('Provide ROS namespace of robot: \n')

def move_repeated():
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    try:
        joint_states = rospy.wait_for_message("/" + rob +"/joint_states", JointState) #what is this doing? this is subscribing to the "joint_states" topic, which is a JointState datatype. who is subscribing to it?
        joints_pos = joint_states.position #positions get flipped here
        print(joints_pos)
        d = 5 #give the arm five seconds to get to the starting point
        g.trajectory.points = [JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0))] #initialize g.trajectory.points
        for i in range(traj.shape[0]):
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=traj[i,:], velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += .008 #seconds between each point
	#print(g.trajectory.points)
        client.send_goal(g)
        client.wait_for_result()
        print(i)
        print(traj[i,:]) #commanded
        print(joint_states.position) #actual
    except KeyboardInterrupt:
        client.cancel_goal()
        raise
    except:
        raise

def main():
    global client
    try:
        rospy.init_node("test_move", anonymous=True, disable_signals=True)
        client = actionlib.SimpleActionClient("/" + rob + "/scaled_pos_joint_traj_controller/follow_joint_trajectory", FollowJointTrajectoryAction)
        print("Waiting for server...")
        client.wait_for_server()
        print("Connected to server")
        parameters = rospy.get_param(None)
        index = str(parameters).find('prefix')
        if (index > 0):
            prefix = str(parameters)[index+len("prefix': '"):(index+len("prefix': '")+str(parameters)[index+len("prefix': '"):-1].find("'"))]
            for i, name in enumerate(JOINT_NAMES):
                JOINT_NAMES[i] = prefix + name
        #print "This program makes the robot move between the following three poses:"
        #print str([Q1[i]*180./pi for i in xrange(0,6)])
        #print str([Q2[i]*180./pi for i in xrange(0,6)])
        #print str([Q3[i]*180./pi for i in xrange(0,6)])
        #print "Please make sure that your robot can move freely between these poses before proceeding!"
        inp = input("Continue? y/n: ")[0]
        if (inp == 'y'):
            move_repeated()
        else:
            print("Halting program")
    except KeyboardInterrupt:
        rospy.signal_shutdown("KeyboardInterrupt")
        raise

if __name__ == '__main__':
    main()
