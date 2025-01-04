"""
The code below is a template for the auto_camera.py file. You will need to
finish the capture() function to take a picture at a given RPY angle. Make
sure you have completed the sensor_calc.py file before you begin this one.
"""

#import libraries
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
import time
import os
import board
import busio
from picamera2 import Picamera2
import numpy as np
import sys
from sensor_calc_V2 import *  # Ensure that you have the sensor_calc_V2 file

#imu and camera initialization
i2c = busio.I2C(board.SCL, board.SDA)
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

#Code to take a picture at a given offset angle
def capture(dir ='roll', target_angle = 70, margin=5):
    #Calibration lines should remain commented out until you implement calibration
    offset_mag = calibrate_mag()
    offset_gyro = calibrate_gyro()
    initial_angle = set_initial(offset_mag)
    
    print("Begin moving camera.")
    
    while True:
        try:
            # Read sensor data
            accelX, accelY, accelZ = accel_gyro.acceleration
            magX, magY, magZ = mag.magnetic

            # Calculate roll, pitch, and yaw
            roll = roll_am(accelX, accelY, accelZ)
            pitch = pitch_am(accelX, accelY, accelZ)
            yaw = yaw_am(accelX, accelY, accelZ, magX, magY, magZ)

            print(f"Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}")
            
            # Apply calibration offsets to magnetometer and gyro values
            magX -= offset_mag[0]
            magY -= offset_mag[1]
            magZ -= offset_mag[2]
            
            gyroX, gyroY, gyroZ = accel_gyro.gyro
            gyroX = gyroX * 180 / np.pi - offset_gyro[0]
            gyroY = gyroY * 180 / np.pi - offset_gyro[1]
            gyroZ = gyroZ * 180 / np.pi - offset_gyro[2]
        
        except Exception as e:
            print(f"Error occurred: {e}")
            break  # Exit the loop if there's an error

        # Choose the direction (roll, pitch, or yaw)
        if dir == 'roll':
            current_angle = roll
        elif dir == 'pitch':
            current_angle = pitch
        elif dir == 'yaw':
            current_angle = yaw
        else:
            print("Invalid direction.")
            break

        # Check if the current angle is within the margin of the target angle
        if abs(current_angle - target_angle) <= margin:
            # Create a new directory called Images and save the new image there
            directory = "/home/miracle2/CubeSat_Software/Images"
            file = "CapturedIMG.jpg"
            path = os.path.join(directory, file)
            
            # Make the directory if it's not already there
            os.makedirs(directory, exist_ok=True)
            
            print(f"Made new directory called {directory}")
            
            # Code to capture image
            print("Capturing image...")

            # Capture the image with picam2
            picam2.start()
            picam2.capture_file(path)  # Capture the image and save it directly to the path
            picam2.stop()
            
            # Message to show success
            print(f"Image captured and saved in {path}")
            break  # Exit the loop after capturing the image
        else:
            # Add a small delay to prevent overloading the CPU
            time.sleep(0.1)

if __name__ == '__main__':
    capture(*sys.argv[1:])
