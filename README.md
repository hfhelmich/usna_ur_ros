# USNA_UR_ROS

HOW TO START UR ROBOT ROS INTERFACE

First go to the UR Robot:
1) Turn on the UR Robot
2) Initialize the robot by powering on and starting it at the initialization screen
3) Click the Setup Robot button then the Network button. In the displayed information, ensure that DHCP is selected, the network is connected, and the IP address is 10.10.130.193. Click back to the main menu after checking.
4) Click the "Run Program" button on the teach pendant
5) From the Run Program screen, click "File -> Load Program" in the top left corner
6) Select the program "ros_control.urp" and click "Open"
7) You will be returned to the Run Program screen and the status will read "Stopped". This is OK for now because the connection to the computer has not yet been made


Go to the computer running the ROS interface code:
1) Open a terminal window
2) Type "roscore" to start the ros core functionality in that terminal
3) Open a new terminal tab or window by pressing "ctrl+shit+t" (for a new tab) or "ctrl+shift+n" (for a new window)
4) In the new window, type the command "roslaunch usna_urx robot_interface_URx.launch" and press enter. This will UDP the connection to the UR robot and begin publishing/receiving topics from the robot.

Return to the UR teach pendant:
1) In the Run Program window, press the play button at the bottom of the screen. You should see a number of variables appear in the table/window on the right side of the screen. The status should change to "Running". The complete system is now ready to use.


HOW TO START MATLAB
Go to the computer:
1) Open a new terminal window or tab
2) Type "matlab" and press enter. Matlab should automatically open.
3) Type "sudo matlab" and press enter to run Matlab as an administrator. Password is "usna1845"

PUSHING GITHUB UPDATES (from here to github):
1) *if necessary* git clone https://github.com/devriesusna/USNA_YASKAWA_ROS_MATLAB.git --> maybe can do git pull
2) username, password = token
3) git status; git add 
4) git commit -m"Message"
5) git push

PUllING GITHUB UPDATES (from github to here):
1) git pull
2) username, password = token
