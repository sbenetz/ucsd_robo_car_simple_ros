#!/usr/bin/python3
import cv2
# from adafruit_servokit import ServoKit



cap = cv2.VideoCapture(0)
cv2.namedWindow('sliders')

def callback(x):
    pass

def slider_to_normalized(slider_input):
    input_start = 0
    input_end = 2000
    output_start = -1
    output_end = 1
    normalized_output = output_start + (slider_input - input_start) * (
            (output_end - output_start) / (input_end - input_start))
    return normalized_output

# THESE VALUES ARE ALL SCALED FOR FINE TUNINING. ACTUAL VALUES RANGE FROM [-1,1]
steer_left = 0
steer_straight = 1000
steer_right = 2000

#THESE VALUES ARE ALL SCALED FOR FINE TUNINING. ACTUAL VALUES RANGE FROM [-1,1]
throttle_reverse = 0
throttle_neutral = 1100
throttle_forward = 2000

cv2.createTrackbar('Steering_value', 'sliders', steer_straight, steer_right, callback)
cv2.createTrackbar('Throttle_value', 'sliders', throttle_neutral, throttle_forward, callback)
print("debug 5")

def test_car():
    try:  
        # Capture the camera feed frame by frame
        # ret, frame = self.cap.read()
        ret, frame = cap.read()
        steer_input = cv2.getTrackbarPos('Steering_value', 'sliders')
        throttle_input = cv2.getTrackbarPos('Throttle_value', 'sliders')
                
        # re-map input values [0,2000] ---> [-1,1] for BOTH throttle and steering
        steering_float = slider_to_normalized(steer_input)
        throttle_float = slider_to_normalized(throttle_input)

        # print(f"\rcurrent steering/throttle: {steering_float}, {throttle_float}", end=" ")

        # Publish re-mapped throttle/steering values
        # kit.servo[1].angle = steering_float # steering servo is on channel 1
        # kit.continuous_servo[2].throttle = throttle_float # DC motor is on channel 2

        # Display the resulting frame
        cv2.imshow('frame', frame)
    except KeyboardInterrupt:  
        break
        
        
    # After the loop release the cap object
    cap.release()
    # self.cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("debug 1")
    test_car()
    print("debug 4")
