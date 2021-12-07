#!/usr/bin/python3
import rospy
from std_msgs.msg import Float32, Float32MultiArray, Bool
from sensor_msgs.msg import LaserScan
import math
import time


OBSTACLE_DETECTION_NODE_NAME = 'simple_obstacle_detection_node'
SUBSCRIBER_TOPIC_NAME = '/scan'
OBSTACLE_DETECTED_TOPIC_NAME = '/obstacle_detection'

class ObstacleDetection:
    def __init__(self):

        self.init_node = rospy.init_node(OBSTACLE_DETECTION_NODE_NAME, anonymous=False)
        self.sub = rospy.Subscriber(SUBSCRIBER_TOPIC_NAME, LaserScan, self.detect_obstacle)
        self.obstacle_pub = rospy.Publisher(OBSTACLE_DETECTED_TOPIC_NAME, Float32MultiArray, queue_size=1)
        self.obstacle_info = Float32MultiArray()

        # Lidar properties (needs to be updated to be ros parameters loaded from config depending on lidar brand)
        self.viewing_angle = 360

        # Obstacle distance limits (meters) (update/calibrate as needed)
        self.max_distance_tolerance = 0.6
        self.min_distance_tolerance = 0.2

        '''
        For LD06
        values at 0 degrees   ---> (straight)
        values at 90 degrees  ---> (full right)
        values at -90 degrees ---> (full left)
        '''

    def detect_obstacle(data):
        total_number_of_scans = len(data.ranges)
        scans_per_degree = int(total_number_of_scans/self.viewing_angle)

        angle_values = [0, 11.5, 22.5, 33.5, 45, 56.5, 67.5, 78.5, 90, 348.5, 337.5, 326.5, 315, 303.5, 292.5, 281.5, 270]
        range_values = []
        for angle in angle_values:
            range_values.append(data.ranges[angle*scans_per_degree])

        min_distance = min(range_values)
        min_angle_index = range_values.index(min(range_values))
        min_angle = angle_values[min_angle_index]

        if max_distance_tolerance >= abs(min_distance) >= min_distance_tolerance:
            angle_rad = (min_angle * math.pi) / 180
            normalized_angle = round(math.sin(angle_rad))
            obstacle_detected = 1.0

            # Publish ROS message
            self.obstacle_info.append(min_distance)
            self.obstacle_info.append(normalized_angle)
            self.obstacle_info.append(obstacle_detected)
            self.obstacle_pub.publish(self.obstacle_detected)

        else:
            # nonsense values
            min_distance = -1.0
            normalized_angle = -1.0
            obstacle_detected = 0.0

            # Publish ROS message
            self.obstacle_info.append(min_distance_data)
            self.obstacle_info.append(normalized_angle)
            self.obstacle_info.append(obstacle_detected)
            self.obstacle_pub.publish(self.obstacle_info)


def main():
    obstacle_detection = ObstacleDetection()
    rate = rospy.Rate(15)
    while not rospy.is_shutdown():
        rospy.spin()
        rate.sleep()


if __name__ == '__main__':
    main()