"""
The code you will write for this module should calculate
roll, pitch, and yaw (RPY) and calibrate your measurements
for better accuracy. Your functions are split into two activities.
The first is basic RPY from the accelerometer and magnetometer. The
second is RPY using the gyroscope. Finally, write the calibration functions.
Run plot.py to test your functions, this is important because auto_camera.py 
relies on your sensor functions here.
"""

#import libraries
import time
import numpy as np
import time
import os
import board
import busio
import math
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL

#imu initialization
i2c = busio.I2C(board.SCL, board.SDA)
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)


#Activity 1: RPY based on accelerometer and magnetometer
def roll_am(accelX,accelY,accelZ):
    #TODO
    roll = math.atan(accelY/(math.sqrt((accelX**2)+(accelZ**2)))) #writing the given functions in python version
    return roll

def pitch_am(accelX,accelY,accelZ):
    #TODO
    pitch = math.atan(accelX/(math.sqrt((accelY**2)+(accelZ**2))))
    return pitch

def yaw_am(accelX,accelY,accelZ,magX,magY,magZ):
    #TODO
    pitch = pitch_am(accelX,accelY,accelZ) #call the above functions to get the roll and pitch values to be used later
    roll = roll_am(accelX,accelY,accelZ)
    
    mag_x = (magX*math.cos(pitch)) + (magY*math.sin(roll)*math.sin(pitch)) + (magZ*math.cos(roll)*math.sin(pitch)) #used the equations given in the pdf
    mag_y = (magY*math.cos(roll)) - (magZ*math.sin(roll))
    
    return (180/np.pi)*np.arctan2(-mag_y, mag_x)

#Activity 2: RPY based on gyroscope
def roll_gy(prev_angle, delT, gyro):
    #TODO
    roll = prev_angle + (gyro[0] * delT) #previous angle added to the product of the gyro value and the delta
    return roll

def pitch_gy(prev_angle, delT, gyro):
    #TODO
    pitch = prev_angle + gyro[1] * delT
    return pitch
def yaw_gy(prev_angle, delT, gyro):
    #TODO
    yaw = prev_angle + gyro[2] * delT
    return yaw

#Activity 3: Sensor calibration
def calibrate_mag():
    #TODO: Set up lists, time, etc
    data = []
    
    print("Preparing to calibrate magnetometer. Please wave around.")
    time.sleep(3)
    
    print("Calibrating...")
    
    for i in range(100): #collects 100 data values
        magX, magY, magZ = mag.magnetic
        data.append([magX, magY, magZ]) #stores these values in x,y,z format (a list)
    
    #TODO: Calculate calibration constants
    print("Calibration complete.")
    x,y,z = zip(*data)
    
    offset_x = (max(x) + min(x)) / 2 #calculating errors and correcting them
    offset_y = (max(y) + min(y)) / 2
    offset_z = (max(z) + min(z)) / 2

    corrected_x = magX - offset_x
    corrected_y = magY - offset_y
    corrected_z = magZ - offset_z
    
    return [corrected_x, corrected_y, corrected_z]

def calibrate_gyro():
    #TODO
    print("Preparing to calibrate gyroscope. Put down the board and do not touch it.")
    time.sleep(3)
    print("Calibrating...")
    
    data = []
    
    for i in range(100):
        gyro = accel_gyro.gyro
        data.append([gyro[0],gyro[1],gyro[2]])
    
    #TODO
    print("Calibration complete.")
    
    x,y,z = zip(*data)
    
    offset_x = (max(x) + min(x)) / 2
    offset_y = (max(y) + min(y)) / 2
    offset_z = (max(z) + min(z)) / 2

    corrected_x = gyro[0] - offset_x
    corrected_y = gyro[1] - offset_y
    corrected_z = gyro[2] - offset_z
    
    return [corrected_x, corrected_y, corrected_z]

def set_initial(mag_offset = [0,0,0]):
    """
    This function is complete. Finds initial RPY values.

    Parameters:
        mag_offset (list): magnetometer calibration offsets
    """
    #Sets the initial position for plotting and gyro calculations.
    print("Preparing to set initial angle. Please hold the IMU still.")
    time.sleep(3)
    print("Setting angle...")
    accelX, accelY, accelZ = accel_gyro.acceleration #m/s^2
    magX, magY, magZ = mag.magnetic #gauss
    #Calibrate magnetometer readings. Defaults to zero until you
    #write the code
    magX = magX - mag_offset[0]
    magY = magY - mag_offset[1]
    magZ = magZ - mag_offset[2]
    
    roll = roll_am(accelX, accelY,accelZ)
    pitch = pitch_am(accelX,accelY,accelZ)
    yaw = yaw_am(accelX,accelY,accelZ,magX,magY,magZ)
    
    print("Initial angle set.")
    return [roll,pitch,yaw]
