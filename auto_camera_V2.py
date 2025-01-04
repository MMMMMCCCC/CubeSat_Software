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
from sensor_calc_V2 import *

#imu and camera initialization
i2c = busio.I2C(board.SCL, board.SDA)
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

#Code to take a picture at a given offset angle
def capture(dir ='roll', target_angle = 70,margin=5):
    #Calibration lines should remain commented out until you implement calibration
    offset_mag = calibrate_mag()
    offset_gyro =calibrate_gyro()
    initial_angle = set_initial(offset_mag)
    prev_angle = initial_angle
    print("Begin moving camera.")
    while True:
        accelX, accelY, accelZ = accel_gyro.acceleration #m/s^2
        magX, magY, magZ = mag.magnetic #gauss
        #Calibrate magnetometer readings
        magX = magX - offset_mag[0]
        magY = magY - offset_mag[1]
        magZ = magZ - offset_mag[2]
        gyroX, gyroY, gyroZ = accel_gyro.gyro #rad/s
        #Convert to degrees and calibrate
        gyroX = gyroX *180/np.pi - offset_gyro[0]
        gyroY = gyroY *180/np.pi - offset_gyro[1]
        gyroZ = gyroZ *180/np.pi - offset_gyro[2]
        
        #TODO: Everything else! Be sure to not take a picture on exactly a
        #certain angle: give yourself some margin for error.
        
        roll = roll_am(accelX, accelY, accelZ)
        pitch = pitch_am(accelX, accelY, accelZ)
        yaw = yaw_am(accelX, accelY, accelZ, magX, magY, magZ)
        
        if dir == 'roll':
            current_angle = roll
        elif dir == 'pitch':
            current_angle = pitch
        elif dir == 'yaw':
            current_angle = yaw
        else:
            print("Invalid direction.")
            break
        
        radians = target_angle * np.pi / 180
        
        if abs(current_angle - radians) <= margin:
            #create a new directory called Images and then save the new image into that directory
            directory = "/home/miracle2/CubeSat_Software/Images"
            file = "CapturedIMG.jpg"
            path = os.path.join(directory, file)
            
            #make the directory if it's not already there
            os.makedirs(directory, exist_ok=True)
            
            print(f"Made new directory called {directory}")
            
            #code to capture image
            print("Capturing image...")
            
            img = picam2.create_still_configuration()
            picam2.start_preview()
            picam2.start(show_preview=True)
            
            time.sleep(1)
            picam2.switch_mode_and_capture_file(img, file)
            
            #message to show success
            print(f"Image captured and saved.")
            picam2.stop()
            break #if image is captured then break out of the loop otherwise keep capturing image

if __name__ == '__main__':
    capture(*sys.argv[1:])
