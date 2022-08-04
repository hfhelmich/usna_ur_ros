% testing ROS startup commands for the UR robots using MATLAB sysem()
% function

LD_path = '/home/ew486f2/UR_ws/devel/lib:/opt/ros/noetic/lib:/opt/ros/noetic/lib/x86_64-linux-gnu';
str = ['export LD_LIBRARY_PATH="' LD_path '";' 'roslaunch usna_urx robot_interface_URx.launch & echo $!']



%%
[sts,cmdout] = system(str)