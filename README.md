# ucsd_robo_car_simple_ros

A simple ROS package using OpenCV on a 1/10 RC car chassis with ackerman steering that can follow a yellow line or stay between two white lines.

<div>

## Table of Contents

- [ucsd_robo_car_simple_ros](#ucsd_robo_car_simple_ros)
  - [Table of Contents](#table-of-contents)
  - [Dependencies](#dependencies)
    - [cv2](#cv2)
    - [adafruit_servokit](#adafruit_servokit)
    - [cv_bridge](#cv_bridge)
  - [Environment Configuration](#environment-configuration)
  - [Package Map](#package-map)
  - [Structure](#structure)
    - [Nodes](#nodes)
      - [**throttle_client**](#throttle_client)
      - [**steering_client**](#steering_client)
      - [**camera_server**](#camera_server)
      - [**line_detection_node**](#line_detection_node)
      - [**lane_detection_node**](#lane_detection_node)
      - [**lane_guidance_node**](#lane_guidance_node)
  - [Topics](#topics)
      - [**steering**](#steering)
      - [**throttle**](#throttle)
      - [**camera_rgb**](#camera_rgb)
      - [**centroid**](#centroid)
  - [Launch](#launch)
  - [Tools](#tools)
    - [**decoder**](#decoder)
    - [**find_camera_values**](#find_camera_values)
  - [Issues and Fixes](#issues-and-fixes)
## Dependencies

### [cv2](https://opencv.org/)

OpenCV is a library, in our case for Python, that provides high-level functions for computer vision and image processing.

### [adafruit_servokit](https://circuitpython.readthedocs.io/projects/servokit/en/latest/)

Adafruit Servokit is a Python library that provides a high-level interface with low-level PWM controls. For this package, the library is used to control PWM servos and a ESC connected to channels of the PCA9685 I2C breakout board.
more details <a href="https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython" >here</a>


### [cv_bridge](http://wiki.ros.org/cv_bridge)

CV Bridge provides functions to easily convert (encode/decode) in between ROS image message types to OpenCV-workable Numpy arrays.

## Environment Configuration

`sudo apt-get update`

`sudo apt-get upgrade`



**1. openCV Setup**

  **a. Check if you have openCV for python3**

   `python3`

   then enter

   `import cv2`

  **b. If no error occurs, you're good to go. Otherwise issue the command below for barebones version**

   `sudo apt-get install python3-pip`

   `pip3 install --upgrade pip`

   `pip3 install opencv-python`


  **c. Check again to see if opencv was compiled correctly for python3**

   `python3`

  then enter

   `import cv2`

**_No errors should have happened, if so, make sure you used pip3 and not pip when running the install command above_**

more details <a href="https://pypi.org/project/opencv-python/" >here</a>

_**if you want to compile from source follow steps below**_

**IF NEEDED**

  **d. build instructions** <a href="https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html" >here</a>



**2. Virtual Environment Setup**

  **a. Creat environment**

   `python3 -m pip install --user virtualenv`

   `sudo apt-get install python3-venv`

   `python3 -m venv --system-site-packages env`

   `source env/bin/activate`

   `python3 -m pip install requests`

  **b. Environment details**

   Get path to executable
   `which python`

   Get python version
   `python --version`

   List of packages
   `pip list`

   Site packages location
   `python -m site`

  **c. Add PYHTHONPATH**

   `nano ~/.bash_profile`

   Add this line to bash file

   `export PYTHONPATH="<path to virtual env>/lib/python3.6"`

  **d. Activate Environment (for new terminals)**

   `source env/bin/activate`

   **NOTE**
   _**WHILE IN VIRTUAL ENVIRONMENT, DO NOT USE "sudo" 
   TO INSTALL PIP PACKAGES, THESE WILL INSTALL TO YOUR 
   LOCAL MACHINE INSTEAD OF VIRTUAL ENVIRONMENT!!!**_

   more details <a href="https://realpython.com/python-virtual-environments-a-primer/" >here</a>
   and <a href="https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html" >here</a>

**3. Upgrading**

`pip install pyyaml`

`pip install rospkg`

`pip install --upgrade pip`

`pip install --upgrade pyinstaller`



**4. Install Adafruit Library**

`pip install adafruit-circuitpython-pca9685`

`pip install adafruit-circuitpython-servokit`

more details <a href="https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython" >here</a>


**5. Access this repository**

  **a. Generate an SSH key and provide it to Gitlab for access to repositories**

   `ssh-keygen # Use all defaults`

  **b. Then press enter until you get to an empty comand line, then**

   `cat $HOME/.ssh/id_rsa.pub`

  **c. Then copy the ssh key and go back to Gitlab. Click on your user profile at the top right corner of the screen then**
     
  **click on settings from the drop down menu. Now a new panel on the left hand side of the screen wil apear, click on SSH Keys,**
     
  **then paste your SSH key into the text field and submit it.**

  **d. Obtain a copy of the repository**

   `git clone git@gitlab.com:djnighti/ucsd_robo_car_simple_ros.git`

  **e. Enter the commands below in the command window on your Jetson:**

   `cd projects/catkin_ws/src`

   `git clone git@gitlab.com:djnighti/ucsdrobocarsimpleros.git`

   `cd ..`

   `catkin_make`

   `source devel/setup.bash`

   `rospack profile`

  **f. Now try this to make sure it was compiled correctly:**

   `roscd ucsd_robo_car_simple_ros`

**If you are brought to this project directory, you are ready to start!**


## Package Map
<img src="ros_overview.png">

## Structure

### Nodes

#### **throttle_client**

Associated file: throttle_client.py

This node subscribes to the [throttle](#Topics) topic. We use subscriber callback function
to validate and normalize throttle value, and then use the [adafruit_servokit](#adafruit_servokit)
module on **channel 0** for sending signals to the hardware.

This node is also responsible for reading and setting the throttle calibration values.

#### **steering_client**

Associated file: steering_client.py

Similar to [throttle_client](#throttle_client), this node subscribes to the [steering](#Topics)
topic and passes the signals to the hardware. The steering servo is on **channel 1**.

<hr>

Plenty of information on how to use the adafruit_servokit libraries can be found <a href="https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython" >here</a> and <a href="https://github.com/adafruit/Adafruit_CircuitPython_ServoKit" >here</a> 



#### **camera_server**

Associated file: camera_server.py

This node simply reads from the camera with cv2's interface and publishes the image to the
[camera_rgb](#Topics) topic. Before publishing, the image is reformatted from the cv image format
so it can be passed through the ROS topic message structure.



#### **line_detection_node**

Associated file: line_detection.py

This node reads from [camera_rgb](#Topics) topic and uses opencv to identify line
information from the image, and publish the information of the middle point of 
a single line to the [centroid](#Topics) topic. The color of line is chosen by the user
and set by using [find_camera_values](#tools)

**Note: The cv windows have been commented out so that no errors occur when running in headless mode. For debugging, its suggested to uncomment these lines.**

#### **lane_detection_node**

Associated file: lane_detection.py

This node has the same functionality as [**line_detection_node**](#line_detection_node) however, now the ability to identify more than one line has been included. It is possible to identify the outside lanes as well as the yellow dashed lines if a green mask is applied which can easily be made by using [**find_camera_values**](#find_camera_values). 

**Note: The cv windows have been commented out so that no errors occur when running in headless mode. For debugging, its suggested to uncomment these lines.**

#### **lane_guidance_node**

Associated file: lane_guidance.py

This node subscribes to the [centroid](#Topics) topic, calculates the throttle and steering
based on the centroid value, and then publish them to their corresponding topics.

Throttle is based on whether or not a centroid exists - car goes faster when centroid is present and slows down when there is none.

Steering is based on a proportional controller implemented by its error function. Gain (Kp) can be tuned in this script.

## Topics


#### **throttle** 
| Name       | Msg Type              | Info                                                       |
| ---------- | --------------------- | ---------------------------------------------------------- |
| throttle   | std_msgs.msg.Float32  | Float value from -1 to 1 for controlling throttle          |


#### **steering**
| Name       | Msg Type              | Info                                                       |
| ---------- | --------------------- | ---------------------------------------------------------- |
| steering   | std_msgs.msg.Float32  | Float value from -1 to 1 for controlling steering          |

#### **camera_rgb**
| Name       | Msg Type              | Info                                                       |
| ---------- | --------------------- | ---------------------------------------------------------- |
| camera_rgb | sensor_msgs.msg.Image | Image last read from USB camera image                      |

#### **centroid**
| Name       | Msg Type              | Info                                                       |
| ---------- | --------------------- | ---------------------------------------------------------- |
| centroid   | std_msgs.msg.Int32MultiArray    | arg 1: Integer for x coordinate of centroid in camera image space arg 2: camera width ex. [centroid,camera_width]|



## Launch

Launching the package is as simple as

`roslaunch ucsd_robo_car_simple_ros simplecv_launch.launch`

This should begin all the necessary nodes and get the car moving.

Or to launch them indvidually, use

`rosrun ucsd_robo_car_simple_ros file_name`

## Tools 


#### **decoder** 

Associated file: decoder.py

This provides a solution for cv_bridge not working and decodes the incoming image into a numpy array that is then passed to the [camera_rgb](#Topics) topic. If cv_bridge is built with python3, then this file is not neccessary.


#### **find_camera_values** 

Associated file: find_camera_values.py

This program allows for the user to quickly tune various camera post-processing parameters including a custom color filter. 
These values need to be **manually** entered into [**line_detection_node**](#line_detection_node) or [**lane_detection_node**](#lane_detection_node) (depending on which you are using) 

| Name       | Msg Type              | Info                                                       |
| ---------- | --------------------- | ---------------------------------------------------------- |
| Hue_low | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| Hue_high | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| Saturation_low | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| Saturation_high | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| Value_low | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| Value_high | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| Hue_low | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| blur_value | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| blur_kernal_value | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| dilation_value | sensor_msgs.msg.Image | Image last read from USB camera image                      |



## Issues and Fixes

### **Error with CV_Bridge conversion from Image message to OpenCV image**

Using **bridge_object.imgmsg_to_cv2()** threw errors on our Jetson Nano environment, so we had to resort to our own image decoder function. Function **decodeImage()** can be imported from **decoder.py**. If you don't want to use our function, the problem can be avoided by properly building CV_Bridge with Python3 in the ROS package.

An alternative solution can be found <a href="https://medium.com/@beta_b0t/how-to-setup-ros-with-python-3-44a69ca36674" >here</a>

### **Throttle not working**

This issue can vary between cars, but generally the problem lies in the battery supply and the PWM range that is mapped by the Adafruit library. If the "start" PWM is too low, then even a maxed out "1" might not map to the PWM value that will trigger the ESC. First make sure the -1 to 1 range is properly calibrated. During runtime, the scale constant found in **throttle_client.py** can also be tuned. As your battery begins to drain, the PWM range becomes under-saturated which decreases performance of the motor. 

**Tip: Always try driving with fully charged battery or periodically recalibrate pwm values manually as motor performance starts decreasing.**


### **ROS version is not compatible with Python3**
If your're having issues using python3, then there is a chance that the virtual environment (explained in `ros_config.txt`) was not setup properly. Try setting up another environment to see if that solves the issue.

More info found 
<a href="https://medium.com/@beta_b0t/how-to-setup-ros-with-python-3-44a69ca36674" >here</a>

