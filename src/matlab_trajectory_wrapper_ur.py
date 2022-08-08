#!/usr/bin/env python3
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

JOINT_NAMES = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

def move_callback(msg):
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    try:
        client = actionlib.SimpleActionClient('scaled_pos_joint_traj_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
        print("Waiting for server...")
        client.wait_for_server()
        print("Connected to server")
        print('waiting for joint states from robot')
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        print("received joint states from robot...")
        print("compiling trajectory from MATLAB")

        d = 5   # Time buffer to allow robot to safely move to first pos

        g.trajectory.points = [JointTrajectoryPoint(positions=joints_pos, velocities=[0]*7, time_from_start=rospy.Duration(0.0))]
        print(msg)
        for i in range(len(msg.points)):
            # velocities=[0]*7
            pos = msg.points[i].positions
            vel = msg.points[i].velocities
            tm = msg.points[i].time_from_start.to_sec()
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=pos, velocities=vel, time_from_start=rospy.Duration(d+tm)))
            #print(g.trajectory.points)
        print("sending goal to rosaction")
        client.send_goal(g)
        client.wait_for_result()
        print("result achieved or error thrown") #actual
    except KeyboardInterrupt:
        client.cancel_goal()
        raise
    except:
        raise


if __name__ == '__main__':
    rospy.init_node("MATLAB_trajectory_wrapper", anonymous=True, disable_signals=True)
    traj_sub = rospy.Subscriber('joint_trajectory_MATLAB',JointTrajectory,move_callback)
    rospy.spin()
