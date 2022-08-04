#!/usr/bin/env python3
#
# Copyright 2015, 2016 Thomas Timm Andersen (original version)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import rospy
import actionlib
import csv
import numpy
from control_msgs.msg import *
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
from math import pi

JOINT_NAMES = ['elbow_joint', 'shoulder_lift_joint', 'shoulder_pan_joint',
               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

client = None

#home position = [0 -90 0 -90 0 0] [0 -1.57 0 -1.57 0 0]

def move1():
    global joints_pos
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    Q1 = [0.0, -1.56, 0.0, -1.56, 0.0, 0.0]
    Q2 = [0.1, -1.56, 0.2, -1.56, 0.0, 0.0]
    Q3 = [0.2, -1.56, 0.1, -1.56, 0.0, 0.0]
    Q4 = [0.3, -1.56, 0.0, -1.56, 0.0, 0.0]
    Q5 = [0.4, -1.56, -0.1, -1.56, 0.0, 0.0]
    Q6 = [0.5, -1.56, -0.2, -1.56, 0.0, 0.0]
    Q7 = [0.6, -1.56, -0.1, -1.56, 0.0, 0.0]
    try:
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        g.trajectory.points = [
            JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0)),
            JointTrajectoryPoint(positions=Q1, velocities=[0]*6, time_from_start=rospy.Duration(1)),
            JointTrajectoryPoint(positions=Q2, velocities=[0]*6, time_from_start=rospy.Duration(1.5)),
            JointTrajectoryPoint(positions=Q3, velocities=[0]*6, time_from_start=rospy.Duration(2)),
	    JointTrajectoryPoint(positions=Q4, velocities=[0]*6, time_from_start=rospy.Duration(2.5)),
	    JointTrajectoryPoint(positions=Q5, velocities=[0]*6, time_from_start=rospy.Duration(3)),
	    JointTrajectoryPoint(positions=Q6, velocities=[0]*6, time_from_start=rospy.Duration(3.5)),
	    JointTrajectoryPoint(positions=Q7, velocities=[0]*6, time_from_start=rospy.Duration(4))]
        client.send_goal(g)
        client.wait_for_result()
    except KeyboardInterrupt:
        client.cancel_goal()
        raise
    except:
        raise

def move_repeated():
    reader = csv.reader(open("trajectory.csv", "rb"), delimiter=",") #open trajectory file
    traj_list = list(reader) #open as a list
    traj = numpy.array(traj_list).astype("float") #convert to float and store in a python array

    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    try:
        print('waiting for joint states from robot')
        joint_states = rospy.wait_for_message("/joint_states", JointState)
        joints_pos = joint_states.position
        print(joints_pos)
        print(type(joints_pos))
        d = 5
        g.trajectory.points = [JointTrajectoryPoint(positions=joints_pos, velocities=[0]*7, time_from_start=rospy.Duration(0.0))]
        print(numpy.shape(traj))
        print(traj[0,:])
        #tmp = tuple(traj[0,:])
        #print(tmp[1:8])
        #print(tmp[8:])
        for i in range(len(traj[:,0])):
            # velocities=[0]*7
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=traj[i,1:8], velocities=traj[i,8:], time_from_start=rospy.Duration(d)))
            d += .05 #seconds between each point
            #print(g.trajectory.points)
        client.send_goal(g)
        client.wait_for_result()
        #print(joint_states.position) #actual
    except KeyboardInterrupt:
        client.cancel_goal()
        raise
    except:
        raise

def main():
    global client
    try:
        rospy.init_node("test_move", anonymous=True, disable_signals=True)
        client = actionlib.SimpleActionClient('scaled_pos_joint_traj_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
        print("Waiting for server...")
        client.wait_for_server()
        print("Connected to server")
        inp = input("Continue? y/n: ")[0]
        if (inp == 'y'):
            move1()
            #move_repeated()
            #move_to()
            #move_disordered()
            #move_interrupt()
        else:
            print("Halting program")
    except KeyboardInterrupt:
        rospy.signal_shutdown("KeyboardInterrupt")
        raise

if __name__ == '__main__':
    main()
